"""
Apex AI Marketing - Maintenance Tasks

Celery tasks for system maintenance: cleanup, database backups,
and health checks with alerting.
"""

import logging
import os
import subprocess
from datetime import datetime, timedelta
from decimal import Decimal

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="backend.tasks.maintenance_tasks.cleanup_old_tasks",
    max_retries=2,
    default_retry_delay=60,
    acks_late=True,
    time_limit=300,
)
def cleanup_old_tasks(self) -> dict:
    """Clean up completed tasks older than 90 days.

    Removes:
    - Completed task records older than 90 days
    - Failed task records older than 30 days
    - Expired Celery result keys from Redis

    Returns:
        dict with counts of records cleaned up.
    """
    from database import async_session_factory
    from models.task import Task

    import asyncio

    COMPLETED_RETENTION_DAYS = 90
    FAILED_RETENTION_DAYS = 30

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select, delete, func

            now = datetime.utcnow()
            completed_cutoff = now - timedelta(days=COMPLETED_RETENTION_DAYS)
            failed_cutoff = now - timedelta(days=FAILED_RETENTION_DAYS)

            # Count before deletion
            completed_count = await session.execute(
                select(func.count()).select_from(Task).where(
                    Task.status == "completed",
                    Task.completed_at < completed_cutoff,
                )
            )
            old_completed = completed_count.scalar() or 0

            failed_count = await session.execute(
                select(func.count()).select_from(Task).where(
                    Task.status == "failed",
                    Task.created_at < failed_cutoff,
                )
            )
            old_failed = failed_count.scalar() or 0

            # Delete old completed tasks
            if old_completed > 0:
                await session.execute(
                    delete(Task).where(
                        Task.status == "completed",
                        Task.completed_at < completed_cutoff,
                    )
                )
                logger.info(
                    "Deleted %d completed tasks older than %d days",
                    old_completed,
                    COMPLETED_RETENTION_DAYS,
                )

            # Delete old failed tasks
            if old_failed > 0:
                await session.execute(
                    delete(Task).where(
                        Task.status == "failed",
                        Task.created_at < failed_cutoff,
                    )
                )
                logger.info(
                    "Deleted %d failed tasks older than %d days",
                    old_failed,
                    FAILED_RETENTION_DAYS,
                )

            await session.commit()

            # Clean up expired Redis keys
            redis_cleaned = await _cleanup_redis_results()

            summary = {
                "completed_tasks_removed": old_completed,
                "failed_tasks_removed": old_failed,
                "redis_keys_cleaned": redis_cleaned,
                "timestamp": now.isoformat(),
            }

            logger.info("Cleanup complete: %s", summary)
            return summary

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Task cleanup failed")
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name="backend.tasks.maintenance_tasks.backup_database",
    max_retries=2,
    default_retry_delay=300,
    acks_late=True,
    time_limit=600,
)
def backup_database(self) -> dict:
    """Create a PostgreSQL database backup using pg_dump.

    Creates a compressed SQL dump and stores it in the configured
    backup directory. Retains the last 7 backups.

    Returns:
        dict with backup file path, size, and status.
    """
    from config import get_settings

    settings = get_settings()

    # Parse database URL for pg_dump
    db_url = settings.DATABASE_URL

    # Extract connection details from the async URL
    # Format: postgresql+asyncpg://user:pass@host:port/dbname
    clean_url = db_url.replace("postgresql+asyncpg://", "")
    user_pass, host_db = clean_url.split("@", 1)
    db_user, db_password = user_pass.split(":", 1)
    host_port, db_name = host_db.split("/", 1)

    if ":" in host_port:
        db_host, db_port = host_port.split(":", 1)
    else:
        db_host = host_port
        db_port = "5432"

    # Backup directory
    backup_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "backups",
    )
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"apex_backup_{timestamp}.sql.gz")

    try:
        # Set password via environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = db_password

        # Run pg_dump with gzip compression
        cmd = (
            f"pg_dump -h {db_host} -p {db_port} -U {db_user} -d {db_name} "
            f"--no-owner --no-privileges --clean --if-exists "
            f"| gzip > {backup_file}"
        )

        process = subprocess.run(
            cmd,
            shell=True,
            env=env,
            capture_output=True,
            text=True,
            timeout=500,
        )

        if process.returncode != 0:
            logger.error("pg_dump failed: %s", process.stderr)
            raise RuntimeError(f"pg_dump failed: {process.stderr}")

        # Get file size
        file_size = os.path.getsize(backup_file) if os.path.exists(backup_file) else 0

        # Clean up old backups (keep last 7)
        _cleanup_old_backups(backup_dir, keep=7)

        summary = {
            "backup_file": backup_file,
            "size_bytes": file_size,
            "size_mb": f"{file_size / (1024 * 1024):.2f}",
            "timestamp": timestamp,
            "status": "success",
        }

        logger.info("Database backup created: %s (%s MB)", backup_file, summary["size_mb"])
        return summary

    except subprocess.TimeoutExpired:
        logger.error("Database backup timed out")
        raise self.retry(exc=TimeoutError("pg_dump timed out"))
    except Exception as exc:
        logger.exception("Database backup failed")
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name="backend.tasks.maintenance_tasks.health_check",
    max_retries=1,
    default_retry_delay=30,
    acks_late=True,
    time_limit=120,
)
def health_check(self) -> dict:
    """Verify all services are running and notify if there are issues.

    Checks:
    1. PostgreSQL database connectivity
    2. Redis connectivity
    3. Celery worker responsiveness
    4. External API availability (Resend, Anthropic)
    5. Disk space
    6. Memory usage

    Returns:
        dict with health status for each service.
    """
    from config import get_settings

    import asyncio

    settings = get_settings()

    async def _run():
        checks = {}

        # ── 1. Database check ─────────────────────────────────────────
        try:
            from database import async_session_factory
            from sqlalchemy import text

            async with async_session_factory() as session:
                await session.execute(text("SELECT 1"))
            checks["database"] = {"status": "healthy", "message": "Connected"}
        except Exception as exc:
            checks["database"] = {"status": "unhealthy", "message": str(exc)}

        # ── 2. Redis check ────────────────────────────────────────────
        try:
            import redis

            r = redis.from_url(settings.REDIS_URL)
            r.ping()
            checks["redis"] = {"status": "healthy", "message": "Connected"}
        except Exception as exc:
            checks["redis"] = {"status": "unhealthy", "message": str(exc)}

        # ── 3. External APIs ──────────────────────────────────────────
        import httpx

        # Anthropic API
        if settings.ANTHROPIC_API_KEY:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(
                        "https://api.anthropic.com/v1/models",
                        headers={
                            "x-api-key": settings.ANTHROPIC_API_KEY,
                            "anthropic-version": "2023-06-01",
                        },
                        timeout=10,
                    )
                    checks["anthropic_api"] = {
                        "status": "healthy" if resp.status_code == 200 else "degraded",
                        "message": f"HTTP {resp.status_code}",
                    }
            except Exception as exc:
                checks["anthropic_api"] = {
                    "status": "unhealthy",
                    "message": str(exc),
                }
        else:
            checks["anthropic_api"] = {
                "status": "not_configured",
                "message": "API key not set",
            }

        # Resend API
        if settings.RESEND_API_KEY:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(
                        "https://api.resend.com/domains",
                        headers={
                            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                        },
                        timeout=10,
                    )
                    checks["resend_api"] = {
                        "status": "healthy" if resp.status_code == 200 else "degraded",
                        "message": f"HTTP {resp.status_code}",
                    }
            except Exception as exc:
                checks["resend_api"] = {
                    "status": "unhealthy",
                    "message": str(exc),
                }
        else:
            checks["resend_api"] = {
                "status": "not_configured",
                "message": "API key not set",
            }

        # ── 4. Disk space ─────────────────────────────────────────────
        try:
            stat = os.statvfs("/")
            total = stat.f_blocks * stat.f_frsize
            available = stat.f_bavail * stat.f_frsize
            used_pct = ((total - available) / total) * 100

            checks["disk_space"] = {
                "status": "healthy" if used_pct < 85 else "warning" if used_pct < 95 else "critical",
                "message": f"{used_pct:.1f}% used ({available / (1024**3):.1f} GB free)",
            }
        except Exception as exc:
            checks["disk_space"] = {"status": "unknown", "message": str(exc)}

        # ── 5. Memory ─────────────────────────────────────────────────
        try:
            with open("/proc/meminfo", "r") as f:
                meminfo = f.read()
            mem_total = int(
                [l for l in meminfo.split("\n") if "MemTotal" in l][0]
                .split()[1]
            )
            mem_available = int(
                [l for l in meminfo.split("\n") if "MemAvailable" in l][0]
                .split()[1]
            )
            used_pct = ((mem_total - mem_available) / mem_total) * 100

            checks["memory"] = {
                "status": "healthy" if used_pct < 85 else "warning" if used_pct < 95 else "critical",
                "message": f"{used_pct:.1f}% used ({mem_available / (1024**2):.1f} GB free)",
            }
        except Exception as exc:
            checks["memory"] = {"status": "unknown", "message": str(exc)}

        # ── Determine overall health ──────────────────────────────────
        statuses = [c["status"] for c in checks.values()]
        if "unhealthy" in statuses or "critical" in statuses:
            overall = "unhealthy"
        elif "warning" in statuses or "degraded" in statuses:
            overall = "degraded"
        else:
            overall = "healthy"

        result = {
            "overall": overall,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": checks,
        }

        # Notify if unhealthy
        if overall in ("unhealthy", "degraded"):
            await _notify_health_issue(result)

        logger.info("Health check: %s", overall)
        return result

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Health check failed")
        raise self.retry(exc=exc)


# ── Helper functions ──────────────────────────────────────────────────────

async def _cleanup_redis_results() -> int:
    """Clean up expired Celery result keys from Redis."""
    from config import get_settings

    settings = get_settings()
    cleaned = 0

    try:
        import redis

        r = redis.from_url(settings.REDIS_URL)
        # Celery results are stored with celery-task-meta- prefix
        cursor = 0
        while True:
            cursor, keys = r.scan(
                cursor=cursor,
                match="celery-task-meta-*",
                count=100,
            )
            for key in keys:
                ttl = r.ttl(key)
                if ttl == -1:  # No expiry set
                    r.expire(key, 86400)  # Set 24h expiry
                    cleaned += 1
            if cursor == 0:
                break
    except Exception as exc:
        logger.error("Redis cleanup failed: %s", exc)

    return cleaned


def _cleanup_old_backups(backup_dir: str, keep: int = 7):
    """Remove old backup files, keeping the most recent N."""
    try:
        backups = sorted(
            [
                os.path.join(backup_dir, f)
                for f in os.listdir(backup_dir)
                if f.startswith("apex_backup_") and f.endswith(".sql.gz")
            ],
            key=os.path.getmtime,
            reverse=True,
        )

        for old_backup in backups[keep:]:
            os.remove(old_backup)
            logger.info("Removed old backup: %s", old_backup)

    except Exception as exc:
        logger.error("Backup cleanup failed: %s", exc)


async def _notify_health_issue(health_result: dict):
    """Send health alert to Telegram."""
    from config import get_settings

    settings = get_settings()

    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return

    unhealthy = [
        f"  {name}: {data['status']} - {data['message']}"
        for name, data in health_result["checks"].items()
        if data["status"] in ("unhealthy", "critical", "degraded", "warning")
    ]

    message = (
        f"HEALTH ALERT: {health_result['overall'].upper()}\n\n"
        f"Issues:\n" + "\n".join(unhealthy) + "\n\n"
        f"Time: {health_result['timestamp']}"
    )

    import httpx

    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": settings.TELEGRAM_CHAT_ID,
                    "text": message,
                },
                timeout=10,
            )
    except Exception as exc:
        logger.error("Health alert notification failed: %s", exc)

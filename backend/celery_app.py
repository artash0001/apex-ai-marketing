"""
Apex AI Marketing - Celery Application Configuration

Configures Celery with Redis broker/backend and beat schedules for all
automated pipelines. All times are in Asia/Dubai timezone (UTC+4).

Dubai work week: Sunday-Thursday.
"""

from celery import Celery
from celery.schedules import crontab

from config import get_settings

settings = get_settings()

# ── Celery app ────────────────────────────────────────────────────────────
celery_app = Celery(
    "apex_ai_marketing",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    # Serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    # Timezone - Dubai (UTC+4)
    timezone="Asia/Dubai",
    enable_utc=True,

    # Task behaviour
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    result_expires=86400,  # 24 hours

    # Retry defaults
    task_default_retry_delay=60,
    task_max_retries=3,

    # Beat schedule - all automated pipelines
    beat_schedule={
        # ── Daily Engine Operations ────────────────────────────────────
        # Runs every day at 7:00 AM Dubai time.
        # Generates scheduled deliverables, checks deadlines, assigns tasks.
        "daily_engine_operations": {
            "task": "backend.tasks.content_tasks.generate_deliverable",
            "schedule": crontab(hour=7, minute=0),
            "kwargs": {},
            "options": {"queue": "engines"},
        },

        # ── Weekly Client Reports ─────────────────────────────────────
        # Every Monday at 8:00 AM Dubai time.
        "weekly_client_reports": {
            "task": "backend.tasks.reporting_tasks.generate_weekly_reports",
            "schedule": crontab(day_of_week=1, hour=8, minute=0),
            "options": {"queue": "reports"},
        },

        # ── Daily Outreach ────────────────────────────────────────────
        # Every day at 9:00 AM Dubai time, Sun-Thu (Dubai work week).
        # day_of_week: 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu
        "daily_outreach": {
            "task": "backend.tasks.outreach_tasks.process_outreach_sequences",
            "schedule": crontab(hour=9, minute=0, day_of_week="0-4"),
            "options": {"queue": "outreach"},
        },

        # ── Experiment Cadence ────────────────────────────────────────
        # Every Wednesday at 9:00 AM Dubai time.
        "experiment_cadence": {
            "task": "backend.tasks.experiment_tasks.check_experiment_status",
            "schedule": crontab(day_of_week=3, hour=9, minute=0),
            "options": {"queue": "experiments"},
        },

        # ── Monthly Billing ───────────────────────────────────────────
        # 1st of each month at 6:00 AM Dubai time.
        "monthly_billing": {
            "task": "backend.tasks.reporting_tasks.generate_monthly_reports",
            "schedule": crontab(day_of_month=1, hour=6, minute=0),
            "options": {"queue": "billing"},
        },

        # ── Daily Maintenance ─────────────────────────────────────────
        # Runs at 3:00 AM Dubai time daily for cleanup and health checks.
        "daily_maintenance_cleanup": {
            "task": "backend.tasks.maintenance_tasks.cleanup_old_tasks",
            "schedule": crontab(hour=3, minute=0),
            "options": {"queue": "maintenance"},
        },

        "daily_health_check": {
            "task": "backend.tasks.maintenance_tasks.health_check",
            "schedule": crontab(hour=3, minute=30),
            "options": {"queue": "maintenance"},
        },

        # ── Weekly Database Backup ────────────────────────────────────
        # Every Friday at 2:00 AM Dubai time.
        "weekly_database_backup": {
            "task": "backend.tasks.maintenance_tasks.backup_database",
            "schedule": crontab(day_of_week=5, hour=2, minute=0),
            "options": {"queue": "maintenance"},
        },

        # ── Propose Next Experiments ──────────────────────────────────
        # Every Wednesday at 10:00 AM Dubai time (after experiment check).
        "propose_next_experiments": {
            "task": "backend.tasks.experiment_tasks.propose_next_experiments",
            "schedule": crontab(day_of_week=3, hour=10, minute=0),
            "options": {"queue": "experiments"},
        },

        # ── Internal Agency Performance Report ────────────────────────
        # Every Sunday at 8:00 AM Dubai time (start of Dubai work week).
        "apex_performance_report": {
            "task": "backend.tasks.reporting_tasks.generate_apex_performance_report",
            "schedule": crontab(day_of_week=0, hour=8, minute=0),
            "options": {"queue": "reports"},
        },
    },

    # Route tasks to dedicated queues
    task_routes={
        "backend.tasks.content_tasks.*": {"queue": "engines"},
        "backend.tasks.outreach_tasks.*": {"queue": "outreach"},
        "backend.tasks.reporting_tasks.*": {"queue": "reports"},
        "backend.tasks.experiment_tasks.*": {"queue": "experiments"},
        "backend.tasks.maintenance_tasks.*": {"queue": "maintenance"},
        "backend.tasks.audit_tasks.*": {"queue": "engines"},
    },
)

# ── Task autodiscovery ────────────────────────────────────────────────────
celery_app.autodiscover_tasks(["tasks"])

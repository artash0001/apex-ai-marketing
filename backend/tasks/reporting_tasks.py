"""
Apex AI Marketing - Reporting Tasks

Celery tasks for generating weekly and monthly client reports,
as well as internal agency performance reports.
"""

import logging
import uuid
from datetime import datetime, date, timedelta
from decimal import Decimal

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="backend.tasks.reporting_tasks.generate_weekly_reports",
    max_retries=2,
    default_retry_delay=120,
    acks_late=True,
    time_limit=1200,
)
def generate_weekly_reports(self) -> dict:
    """Generate weekly performance reports for all active clients.

    For each active client with running engine engagements:
    1. Gather metrics from the past 7 days
    2. Compare against KPI targets
    3. Render the weekly report template
    4. Store as a deliverable
    5. Send via email if configured

    Returns:
        dict with count of reports generated and any errors.
    """
    from database import async_session_factory
    from models.client import Client
    from models.project import EngineEngagement
    from models.content import Deliverable
    from templates.reports.weekly_report_template import render_weekly_report

    import asyncio

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select

            # Fetch active clients with engagements
            result = await session.execute(
                select(Client).where(Client.status == "active")
            )
            clients = result.scalars().all()

            reports_generated = 0
            errors = []
            report_ids = []

            today = date.today()
            week_start = today - timedelta(days=7)

            for client in clients:
                try:
                    # Fetch active engagements
                    eng_result = await session.execute(
                        select(EngineEngagement).where(
                            EngineEngagement.client_id == client.id,
                            EngineEngagement.status == "active",
                        )
                    )
                    engagements = eng_result.scalars().all()

                    if not engagements:
                        continue

                    # ── Gather metrics ────────────────────────────────
                    metrics = await _gather_weekly_metrics(
                        session, client, engagements, week_start, today
                    )

                    # ── Render report ─────────────────────────────────
                    report_markdown = render_weekly_report(
                        client_name=client.name,
                        company=client.company or "",
                        week_start=week_start.isoformat(),
                        week_end=today.isoformat(),
                        engagements=[
                            {
                                "engine_name": e.engine_name,
                                "status": e.status,
                                "kpi_targets": e.kpi_targets or {},
                            }
                            for e in engagements
                        ],
                        metrics=metrics,
                        language=client.language or "en",
                    )

                    # ── Store as deliverable ──────────────────────────
                    deliverable = Deliverable(
                        client_id=client.id,
                        type="report",
                        title=f"Weekly Report: {client.company or client.name} ({week_start} to {today})",
                        body=report_markdown,
                        meta_data={
                            "report_type": "weekly",
                            "week_start": week_start.isoformat(),
                            "week_end": today.isoformat(),
                            "metrics": metrics,
                        },
                        status="in_review",
                        ai_agent_used="reporting",
                        language=client.language or "en",
                    )
                    session.add(deliverable)
                    await session.flush()

                    report_ids.append(str(deliverable.id))
                    reports_generated += 1

                    # ── Send via email ────────────────────────────────
                    if client.email:
                        await _send_report_email(
                            client=client,
                            report_markdown=report_markdown,
                            report_type="weekly",
                        )

                    logger.info(
                        "Weekly report generated for %s (%s)",
                        client.name,
                        client.company,
                    )

                except Exception as exc:
                    logger.error(
                        "Failed to generate weekly report for %s: %s",
                        client.name,
                        exc,
                    )
                    errors.append(
                        {"client": client.name, "error": str(exc)}
                    )

            await session.commit()

            return {
                "reports_generated": reports_generated,
                "report_ids": report_ids,
                "errors": errors,
                "week": f"{week_start} to {today}",
            }

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Weekly report generation failed")
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name="backend.tasks.reporting_tasks.generate_monthly_reports",
    max_retries=2,
    default_retry_delay=300,
    acks_late=True,
    time_limit=1800,
)
def generate_monthly_reports(self) -> dict:
    """Generate monthly reports with billing for all active clients.

    For each active client:
    1. Generate comprehensive monthly performance report
    2. Calculate billing based on active engines
    3. Create invoice record
    4. Send report and invoice via email

    Returns:
        dict with counts of reports and invoices generated.
    """
    from database import async_session_factory
    from models.client import Client
    from models.project import EngineEngagement
    from models.content import Deliverable
    from models.invoice import Invoice
    from templates.reports.monthly_report_template import render_monthly_report

    import asyncio

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select

            result = await session.execute(
                select(Client).where(Client.status == "active")
            )
            clients = result.scalars().all()

            reports_generated = 0
            invoices_created = 0
            errors = []

            today = date.today()
            month_start = today.replace(day=1)
            prev_month_end = month_start - timedelta(days=1)
            prev_month_start = prev_month_end.replace(day=1)

            for client in clients:
                try:
                    # Fetch active engagements
                    eng_result = await session.execute(
                        select(EngineEngagement).where(
                            EngineEngagement.client_id == client.id,
                            EngineEngagement.status == "active",
                        )
                    )
                    engagements = eng_result.scalars().all()

                    if not engagements:
                        continue

                    # ── Gather monthly metrics ────────────────────────
                    metrics = await _gather_monthly_metrics(
                        session, client, engagements,
                        prev_month_start, prev_month_end,
                    )

                    # ── Render monthly report ─────────────────────────
                    report_markdown = render_monthly_report(
                        client_name=client.name,
                        company=client.company or "",
                        month_start=prev_month_start.isoformat(),
                        month_end=prev_month_end.isoformat(),
                        engagements=[
                            {
                                "engine_name": e.engine_name,
                                "status": e.status,
                                "monthly_price": str(e.monthly_price or 0),
                                "kpi_targets": e.kpi_targets or {},
                            }
                            for e in engagements
                        ],
                        metrics=metrics,
                        language=client.language or "en",
                    )

                    # Store report
                    report_deliverable = Deliverable(
                        client_id=client.id,
                        type="report",
                        title=(
                            f"Monthly Report: {client.company or client.name} "
                            f"({prev_month_start.strftime('%B %Y')})"
                        ),
                        body=report_markdown,
                        meta_data={
                            "report_type": "monthly",
                            "month_start": prev_month_start.isoformat(),
                            "month_end": prev_month_end.isoformat(),
                            "metrics": metrics,
                        },
                        status="in_review",
                        ai_agent_used="reporting",
                        language=client.language or "en",
                    )
                    session.add(report_deliverable)
                    reports_generated += 1

                    # ── Create invoice ────────────────────────────────
                    total_amount = sum(
                        e.monthly_price or Decimal("0")
                        for e in engagements
                    )

                    if total_amount > 0:
                        invoice = Invoice(
                            client_id=client.id,
                            amount=total_amount,
                            currency="USD",
                            status="draft",
                            due_date=today + timedelta(days=14),
                            items={
                                "engines": [
                                    {
                                        "name": e.engine_name,
                                        "amount": str(e.monthly_price or 0),
                                    }
                                    for e in engagements
                                ],
                                "period": f"{prev_month_start} to {prev_month_end}",
                            },
                            notes=f"Monthly invoice for {prev_month_start.strftime('%B %Y')}",
                        )
                        session.add(invoice)
                        invoices_created += 1

                    # ── Send email ────────────────────────────────────
                    if client.email:
                        await _send_report_email(
                            client=client,
                            report_markdown=report_markdown,
                            report_type="monthly",
                        )

                    logger.info(
                        "Monthly report + invoice for %s (%s)",
                        client.name,
                        client.company,
                    )

                except Exception as exc:
                    logger.error(
                        "Monthly report failed for %s: %s",
                        client.name,
                        exc,
                    )
                    errors.append(
                        {"client": client.name, "error": str(exc)}
                    )

            await session.commit()

            return {
                "reports_generated": reports_generated,
                "invoices_created": invoices_created,
                "period": f"{prev_month_start} to {prev_month_end}",
                "errors": errors,
            }

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Monthly report generation failed")
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name="backend.tasks.reporting_tasks.generate_apex_performance_report",
    max_retries=2,
    default_retry_delay=120,
    acks_late=True,
)
def generate_apex_performance_report(self) -> dict:
    """Generate internal agency performance report.

    Tracks:
    - Total active clients and MRR
    - Pipeline health (leads, audits, proposals)
    - Engine utilization rates
    - AI cost tracking
    - Outreach performance (open rates, reply rates)
    - Client satisfaction indicators
    - Team workload distribution

    Returns:
        dict with the complete performance report data.
    """
    from database import async_session_factory
    from models.client import Client
    from models.lead import Lead
    from models.project import EngineEngagement
    from models.content import Deliverable
    from models.invoice import Invoice
    from models.experiment import Experiment

    import asyncio

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select, func

            today = date.today()
            week_ago = today - timedelta(days=7)
            month_ago = today - timedelta(days=30)

            # ── Client metrics ────────────────────────────────────────
            active_clients = await session.execute(
                select(func.count()).select_from(Client).where(
                    Client.status == "active"
                )
            )
            active_count = active_clients.scalar() or 0

            total_mrr = await session.execute(
                select(func.sum(EngineEngagement.monthly_price)).where(
                    EngineEngagement.status == "active"
                )
            )
            mrr = total_mrr.scalar() or Decimal("0")

            # ── Pipeline metrics ──────────────────────────────────────
            pipeline_counts = {}
            for status in ["lead", "audit_requested", "audit_delivered", "active"]:
                count_result = await session.execute(
                    select(func.count()).select_from(Client).where(
                        Client.status == status
                    )
                )
                pipeline_counts[status] = count_result.scalar() or 0

            # ── Outreach metrics ──────────────────────────────────────
            new_leads = await session.execute(
                select(func.count()).select_from(Lead).where(
                    Lead.created_at >= month_ago
                )
            )
            new_leads_count = new_leads.scalar() or 0

            replied_leads = await session.execute(
                select(func.count()).select_from(Lead).where(
                    Lead.outreach_status == "replied",
                    Lead.created_at >= month_ago,
                )
            )
            replied_count = replied_leads.scalar() or 0

            # ── Deliverable metrics ───────────────────────────────────
            deliverables_this_week = await session.execute(
                select(func.count()).select_from(Deliverable).where(
                    Deliverable.created_at >= week_ago
                )
            )
            weekly_deliverables = deliverables_this_week.scalar() or 0

            # ── AI cost tracking ──────────────────────────────────────
            ai_cost_month = await session.execute(
                select(func.sum(Deliverable.ai_cost)).where(
                    Deliverable.created_at >= month_ago
                )
            )
            monthly_ai_cost = ai_cost_month.scalar() or Decimal("0")

            # ── Experiments ───────────────────────────────────────────
            running_experiments = await session.execute(
                select(func.count()).select_from(Experiment).where(
                    Experiment.status == "running"
                )
            )
            running_exp_count = running_experiments.scalar() or 0

            # ── Compile report ────────────────────────────────────────
            report = {
                "generated_at": datetime.utcnow().isoformat(),
                "period": f"{week_ago} to {today}",
                "client_metrics": {
                    "active_clients": active_count,
                    "monthly_recurring_revenue": str(mrr),
                    "pipeline": pipeline_counts,
                },
                "outreach_metrics": {
                    "new_leads_30d": new_leads_count,
                    "replied_30d": replied_count,
                    "reply_rate": (
                        f"{(replied_count / new_leads_count * 100):.1f}%"
                        if new_leads_count > 0
                        else "N/A"
                    ),
                },
                "delivery_metrics": {
                    "deliverables_this_week": weekly_deliverables,
                    "ai_cost_30d": str(monthly_ai_cost),
                },
                "experiments": {
                    "running": running_exp_count,
                },
            }

            # Send to Telegram
            await _notify_performance_report(report)

            logger.info("Apex performance report generated: %s", report)

            return report

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Performance report generation failed")
        raise self.retry(exc=exc)


# ── Helper functions ──────────────────────────────────────────────────────

async def _gather_weekly_metrics(
    session, client, engagements, week_start, week_end
) -> dict:
    """Gather performance metrics for the past week.

    TODO: Integrate with analytics APIs (Google Analytics, Search Console, etc.)
    """
    from models.content import Deliverable
    from sqlalchemy import select, func

    # Count deliverables produced this week
    del_count = await session.execute(
        select(func.count()).select_from(Deliverable).where(
            Deliverable.client_id == client.id,
            Deliverable.created_at >= week_start,
        )
    )

    return {
        "deliverables_produced": del_count.scalar() or 0,
        "engines_active": len(engagements),
        "kpi_progress": {},
        "highlights": [],
        "action_items": [],
    }


async def _gather_monthly_metrics(
    session, client, engagements, month_start, month_end
) -> dict:
    """Gather performance metrics for the past month.

    TODO: Integrate with analytics APIs.
    """
    from models.content import Deliverable
    from models.experiment import Experiment
    from sqlalchemy import select, func

    del_count = await session.execute(
        select(func.count()).select_from(Deliverable).where(
            Deliverable.client_id == client.id,
            Deliverable.created_at >= month_start,
        )
    )

    exp_count = await session.execute(
        select(func.count()).select_from(Experiment).where(
            Experiment.client_id == client.id,
            Experiment.created_at >= month_start,
        )
    )

    return {
        "deliverables_produced": del_count.scalar() or 0,
        "experiments_run": exp_count.scalar() or 0,
        "engines_active": len(engagements),
        "kpi_progress": {},
        "roi_indicators": {},
        "highlights": [],
        "next_month_priorities": [],
    }


async def _send_report_email(client, report_markdown: str, report_type: str):
    """Send report delivery email to the client."""
    from config import get_settings
    from templates.emails.report_delivery import get_report_email

    settings = get_settings()

    if not settings.RESEND_API_KEY or not client.email:
        logger.info(
            "Skipping email for %s (API key or email missing)", client.name
        )
        return

    email_content = get_report_email(
        client_name=client.name,
        company=client.company or "",
        report_type=report_type,
        language=client.language or "en",
    )

    import httpx

    async with httpx.AsyncClient() as http_client:
        await http_client.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": f"{settings.FROM_NAME} <{settings.FROM_EMAIL}>",
                "to": [client.email],
                "subject": email_content["subject"],
                "html": email_content["body"],
            },
            timeout=15,
        )


async def _notify_performance_report(report: dict):
    """Send performance report summary to Telegram."""
    from config import get_settings

    settings = get_settings()

    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return

    message = (
        "APEX PERFORMANCE REPORT\n\n"
        f"Period: {report['period']}\n\n"
        f"Clients: {report['client_metrics']['active_clients']} active\n"
        f"MRR: ${report['client_metrics']['monthly_recurring_revenue']}\n\n"
        f"Pipeline:\n"
    )
    for status, count in report["client_metrics"]["pipeline"].items():
        message += f"  {status}: {count}\n"

    message += (
        f"\nOutreach (30d):\n"
        f"  New leads: {report['outreach_metrics']['new_leads_30d']}\n"
        f"  Reply rate: {report['outreach_metrics']['reply_rate']}\n\n"
        f"Delivery:\n"
        f"  Deliverables this week: {report['delivery_metrics']['deliverables_this_week']}\n"
        f"  AI cost (30d): ${report['delivery_metrics']['ai_cost_30d']}\n"
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
        logger.error("Failed to send performance report to Telegram: %s", exc)

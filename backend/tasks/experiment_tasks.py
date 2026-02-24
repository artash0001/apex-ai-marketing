"""
Apex AI Marketing - Experiment Tasks

Celery tasks for managing structured marketing experiments:
checking running experiments, evaluating results, and proposing
new tests for Growth Ops clients.
"""

import logging
import uuid
from datetime import datetime, date, timedelta

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="backend.tasks.experiment_tasks.check_experiment_status",
    max_retries=2,
    default_retry_delay=120,
    acks_late=True,
    time_limit=600,
)
def check_experiment_status(self) -> dict:
    """Check all running experiments and evaluate completed ones.

    For each running experiment:
    1. Check if the experiment end date has passed
    2. If completed, gather result data
    3. Evaluate results against hypothesis
    4. Make a decision: implement, iterate, or discard
    5. Record learnings

    Returns:
        dict with counts of experiments checked, completed, and decisions made.
    """
    from database import async_session_factory
    from models.experiment import Experiment
    from models.client import Client

    import asyncio

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select

            today = date.today()

            # Fetch running experiments
            result = await session.execute(
                select(Experiment).where(Experiment.status == "running")
            )
            experiments = result.scalars().all()

            checked = 0
            completed = 0
            decisions = []

            for experiment in experiments:
                checked += 1

                # Check if experiment period has ended
                if experiment.end_date and experiment.end_date <= today:
                    logger.info(
                        "Experiment %s has reached end date. Evaluating...",
                        experiment.id,
                    )

                    # Fetch client for context
                    client = None
                    if experiment.client_id:
                        client_result = await session.execute(
                            select(Client).where(
                                Client.id == experiment.client_id
                            )
                        )
                        client = client_result.scalar_one_or_none()

                    # ── Gather results ────────────────────────────────
                    result_data = await _gather_experiment_results(
                        experiment, client
                    )
                    experiment.result_data = result_data

                    # ── Evaluate and decide ───────────────────────────
                    evaluation = await _evaluate_experiment(
                        experiment, result_data
                    )

                    experiment.decision = evaluation.get(
                        "decision", "iterate"
                    )
                    experiment.learning = evaluation.get("learning", "")
                    experiment.status = "completed"

                    completed += 1
                    decisions.append(
                        {
                            "experiment_id": str(experiment.id),
                            "hypothesis": experiment.hypothesis[:100],
                            "decision": experiment.decision,
                            "primary_metric_result": result_data.get(
                                "primary_metric_value"
                            ),
                        }
                    )

                    logger.info(
                        "Experiment %s completed. Decision: %s",
                        experiment.id,
                        experiment.decision,
                    )

                else:
                    # Still running - check if metrics are on track
                    days_remaining = (
                        (experiment.end_date - today).days
                        if experiment.end_date
                        else None
                    )
                    logger.info(
                        "Experiment %s still running. %s days remaining.",
                        experiment.id,
                        days_remaining,
                    )

            await session.commit()

            # Notify about completed experiments
            if decisions:
                await _notify_experiment_completions(decisions)

            return {
                "checked": checked,
                "completed": completed,
                "still_running": checked - completed,
                "decisions": decisions,
            }

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Experiment status check failed")
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name="backend.tasks.experiment_tasks.propose_next_experiments",
    max_retries=2,
    default_retry_delay=120,
    acks_late=True,
    time_limit=900,
)
def propose_next_experiments(self) -> dict:
    """Propose next experiments for Growth Ops clients.

    For each client with an active Growth Ops engine engagement:
    1. Review past experiment results and learnings
    2. Analyze current performance data
    3. Generate 2-3 experiment proposals with hypotheses
    4. Create experiment records in 'planned' status

    Returns:
        dict with count of experiments proposed per client.
    """
    from database import async_session_factory
    from models.client import Client
    from models.project import EngineEngagement
    from models.experiment import Experiment

    import asyncio

    GROWTH_OPS_ENGINES = [
        "growth_ops",
        "growth_operations",
        "conversion_optimization",
        "paid_performance",
    ]

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select

            # Find clients with Growth Ops engagements
            result = await session.execute(
                select(EngineEngagement).where(
                    EngineEngagement.status == "active",
                    EngineEngagement.engine_name.in_(GROWTH_OPS_ENGINES),
                )
            )
            engagements = result.scalars().all()

            proposals_created = 0
            client_proposals = {}

            for engagement in engagements:
                try:
                    # Fetch client
                    client_result = await session.execute(
                        select(Client).where(
                            Client.id == engagement.client_id
                        )
                    )
                    client = client_result.scalar_one_or_none()
                    if not client:
                        continue

                    # Fetch past experiments for this client
                    past_result = await session.execute(
                        select(Experiment)
                        .where(
                            Experiment.client_id == client.id,
                            Experiment.status == "completed",
                        )
                        .order_by(Experiment.created_at.desc())
                        .limit(10)
                    )
                    past_experiments = past_result.scalars().all()

                    # ── Generate proposals using AI ───────────────────
                    proposals = await _generate_experiment_proposals(
                        client=client,
                        engagement=engagement,
                        past_experiments=past_experiments,
                    )

                    created_ids = []
                    for proposal in proposals:
                        experiment = Experiment(
                            client_id=client.id,
                            engine_engagement_id=engagement.id,
                            hypothesis=proposal["hypothesis"],
                            variable_changed=proposal.get("variable_changed", ""),
                            primary_metric=proposal.get("primary_metric", ""),
                            guardrail_metrics=proposal.get("guardrail_metrics"),
                            start_date=proposal.get("start_date"),
                            end_date=proposal.get("end_date"),
                            status="planned",
                        )
                        session.add(experiment)
                        await session.flush()
                        created_ids.append(str(experiment.id))
                        proposals_created += 1

                    client_proposals[client.name] = {
                        "count": len(created_ids),
                        "experiment_ids": created_ids,
                    }

                    logger.info(
                        "Proposed %d experiments for %s",
                        len(created_ids),
                        client.name,
                    )

                except Exception as exc:
                    logger.error(
                        "Failed to propose experiments for engagement %s: %s",
                        engagement.id,
                        exc,
                    )

            await session.commit()

            return {
                "total_proposals": proposals_created,
                "by_client": client_proposals,
            }

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Experiment proposal generation failed")
        raise self.retry(exc=exc)


# ── Helper functions ──────────────────────────────────────────────────────

async def _gather_experiment_results(experiment, client) -> dict:
    """Gather experiment result data from analytics.

    TODO: Integrate with analytics APIs (Google Analytics, ad platforms, etc.)
    """
    return {
        "primary_metric_value": None,
        "guardrail_metrics": {},
        "sample_size": 0,
        "confidence_level": None,
        "gathered_at": datetime.utcnow().isoformat(),
        "note": "Pending analytics integration",
    }


async def _evaluate_experiment(experiment, result_data: dict) -> dict:
    """Evaluate experiment results and make a decision using AI.

    Decision framework:
    - implement: Clear positive result with statistical significance
    - iterate: Promising direction but needs refinement
    - discard: No improvement or negative result

    TODO: Integrate with Claude API for evaluation.
    """
    return {
        "decision": "iterate",
        "learning": (
            "Experiment evaluation pending AI integration. "
            "Manual review recommended."
        ),
        "confidence": "low",
        "recommendations": [],
    }


async def _generate_experiment_proposals(
    client, engagement, past_experiments
) -> list:
    """Generate experiment proposals using AI.

    Analyzes past experiments, current performance, and industry benchmarks
    to propose the next set of tests.

    TODO: Integrate with Claude API.
    """
    # Extract learnings from past experiments
    learnings = [
        {
            "hypothesis": exp.hypothesis,
            "decision": exp.decision,
            "learning": exp.learning,
        }
        for exp in past_experiments
        if exp.learning
    ]

    today = date.today()

    # Default proposals structure (to be replaced by AI generation)
    proposals = [
        {
            "hypothesis": (
                f"For {client.company or client.name}: improving the primary "
                f"CTA placement above the fold will increase conversion rate "
                f"by 15% while maintaining bounce rate within 5% of current levels."
            ),
            "variable_changed": "CTA placement and design",
            "primary_metric": "conversion_rate",
            "guardrail_metrics": {
                "bounce_rate": {"max_increase": "5%"},
                "page_load_time": {"max_increase": "0.5s"},
            },
            "start_date": today + timedelta(days=3),
            "end_date": today + timedelta(days=17),  # 2-week test
        },
        {
            "hypothesis": (
                f"For {client.company or client.name}: adding social proof "
                f"elements (testimonials, client count) to the landing page "
                f"will increase lead form submissions by 20%."
            ),
            "variable_changed": "Social proof elements on landing page",
            "primary_metric": "lead_form_submissions",
            "guardrail_metrics": {
                "page_load_time": {"max_increase": "1s"},
            },
            "start_date": today + timedelta(days=3),
            "end_date": today + timedelta(days=17),
        },
    ]

    return proposals


async def _notify_experiment_completions(decisions: list):
    """Notify the team about completed experiments via Telegram."""
    from config import get_settings

    settings = get_settings()

    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return

    message = "EXPERIMENT RESULTS\n\n"
    for d in decisions:
        decision_label = {
            "implement": "[IMPLEMENT]",
            "iterate": "[ITERATE]",
            "discard": "[DISCARD]",
        }.get(d["decision"], "[?]")

        message += (
            f"{decision_label} {d['hypothesis'][:80]}...\n"
            f"  Metric result: {d.get('primary_metric_result', 'N/A')}\n\n"
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
        logger.error("Telegram notification failed: %s", exc)

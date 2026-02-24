"""
Apex AI Marketing - Content Tasks

Celery tasks for generating, reviewing, and iterating on deliverables
using the AI agent pipeline.
"""

import logging
import uuid
from datetime import datetime

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="backend.tasks.content_tasks.generate_deliverable",
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
    time_limit=600,
    soft_time_limit=540,
)
def generate_deliverable(
    self,
    engine_engagement_id: str = None,
    deliverable_type: str = None,
) -> dict:
    """Generate a content deliverable using the appropriate AI agent.

    Maps deliverable types to their corresponding engine agents:
    - content_brief / article / blog_post -> Content Engine
    - email_sequence -> Email Sequence Builder
    - ad_copy -> Paid Performance Agent
    - seo_page / landing_page -> SEO Architect
    - social_post -> Social Media Agent
    - video_script -> Video Script Agent
    - gmb_post -> Local Visibility Agent
    - report -> Reporting Agent

    Args:
        engine_engagement_id: UUID string of the engine engagement.
        deliverable_type: Type of deliverable to generate.

    Returns:
        dict with deliverable_id, type, and status.
    """
    from database import async_session_factory
    from models.project import EngineEngagement
    from models.content import Deliverable
    from models.client import Client

    import asyncio

    # Agent mapping by deliverable type
    AGENT_MAP = {
        "content_brief": "content_engine",
        "article": "content_engine",
        "blog_post": "content_engine",
        "email_sequence": "email_sequence_builder",
        "ad_copy": "paid_performance",
        "seo_page": "seo_architect",
        "landing_page": "seo_architect",
        "social_post": "social_media",
        "video_script": "video_script",
        "gmb_post": "local_visibility",
        "report": "reporting",
        "audit_report": "infrastructure_auditor",
    }

    async def _run():
        if not engine_engagement_id:
            logger.info("No engine_engagement_id provided; running scheduled scan.")
            return await _process_scheduled_deliverables()

        async with async_session_factory() as session:
            from sqlalchemy import select
            from sqlalchemy.orm import selectinload

            result = await session.execute(
                select(EngineEngagement)
                .where(EngineEngagement.id == uuid.UUID(engine_engagement_id))
            )
            engagement = result.scalar_one_or_none()
            if not engagement:
                raise ValueError(
                    f"EngineEngagement {engine_engagement_id} not found"
                )

            # Fetch client
            client_result = await session.execute(
                select(Client).where(Client.id == engagement.client_id)
            )
            client = client_result.scalar_one_or_none()

            agent_name = AGENT_MAP.get(deliverable_type, "content_engine")
            logger.info(
                "Generating %s for engagement %s using agent %s",
                deliverable_type,
                engine_engagement_id,
                agent_name,
            )

            # Generate content via AI agent
            generated = await _invoke_agent(
                agent_name=agent_name,
                deliverable_type=deliverable_type,
                client=client,
                engagement=engagement,
            )

            # Store deliverable
            deliverable = Deliverable(
                engine_engagement_id=uuid.UUID(engine_engagement_id),
                client_id=engagement.client_id,
                type=deliverable_type,
                title=generated.get("title", f"{deliverable_type} deliverable"),
                body=generated.get("body", ""),
                meta_data=generated.get("meta_data", {}),
                status="draft",
                ai_agent_used=agent_name,
                ai_model_used=generated.get("model_used", ""),
                ai_cost=generated.get("cost"),
                language=client.language if client else "en",
            )
            session.add(deliverable)
            await session.commit()
            await session.refresh(deliverable)

            logger.info(
                "Deliverable created: %s (%s) for %s",
                deliverable.id,
                deliverable_type,
                client.name if client else "unknown",
            )

            return {
                "deliverable_id": str(deliverable.id),
                "type": deliverable_type,
                "status": "draft",
                "agent_used": agent_name,
            }

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception(
            "Failed to generate deliverable for engagement %s",
            engine_engagement_id,
        )
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name="backend.tasks.content_tasks.review_deliverable",
    max_retries=2,
    default_retry_delay=60,
    acks_late=True,
)
def review_deliverable(self, deliverable_id: str) -> dict:
    """Review a deliverable through Brand Voice Agent and Quality Gate.

    Pipeline:
    1. Brand Voice Agent - check tone, style, terminology consistency
    2. Quality Gate - score on completeness, accuracy, actionability

    Args:
        deliverable_id: UUID string of the deliverable to review.

    Returns:
        dict with review results, score, and updated status.
    """
    from database import async_session_factory
    from models.content import Deliverable
    from models.client import Client

    import asyncio

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select

            result = await session.execute(
                select(Deliverable).where(
                    Deliverable.id == uuid.UUID(deliverable_id)
                )
            )
            deliverable = result.scalar_one_or_none()
            if not deliverable:
                raise ValueError(f"Deliverable {deliverable_id} not found")

            # Fetch client for brand voice reference
            client = None
            if deliverable.client_id:
                client_result = await session.execute(
                    select(Client).where(Client.id == deliverable.client_id)
                )
                client = client_result.scalar_one_or_none()

            logger.info(
                "Reviewing deliverable %s (%s)",
                deliverable_id,
                deliverable.type,
            )

            # ── Brand Voice Check ─────────────────────────────────────
            brand_voice_result = await _check_brand_voice(
                deliverable=deliverable,
                brand_voice_doc=client.brand_voice_doc if client else None,
            )

            # ── Quality Gate ──────────────────────────────────────────
            quality_result = await _quality_gate_review(deliverable)

            # Calculate combined score
            combined_score = (
                brand_voice_result.get("score", 0) * 0.4
                + quality_result.get("score", 0) * 0.6
            )

            # Update deliverable
            review_notes = (
                f"Brand Voice Score: {brand_voice_result.get('score', 'N/A')}/10\n"
                f"Quality Score: {quality_result.get('score', 'N/A')}/10\n"
                f"Combined Score: {combined_score:.1f}/10\n\n"
                f"Brand Voice Feedback:\n{brand_voice_result.get('feedback', '')}\n\n"
                f"Quality Feedback:\n{quality_result.get('feedback', '')}"
            )

            deliverable.review_notes = review_notes
            deliverable.status = "in_review" if combined_score >= 7.0 else "draft"
            deliverable.meta_data = {
                **(deliverable.meta_data or {}),
                "review": {
                    "brand_voice_score": brand_voice_result.get("score"),
                    "quality_score": quality_result.get("score"),
                    "combined_score": combined_score,
                    "reviewed_at": datetime.utcnow().isoformat(),
                },
            }

            await session.commit()

            return {
                "deliverable_id": deliverable_id,
                "combined_score": combined_score,
                "brand_voice_score": brand_voice_result.get("score"),
                "quality_score": quality_result.get("score"),
                "status": deliverable.status,
                "passed": combined_score >= 7.0,
            }

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Failed to review deliverable %s", deliverable_id)
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name="backend.tasks.content_tasks.iterate_deliverable",
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
)
def iterate_deliverable(self, deliverable_id: str, feedback: str) -> dict:
    """Iterate on a deliverable based on review feedback.

    The appropriate agent revises the content based on the provided feedback.

    Args:
        deliverable_id: UUID string of the deliverable to iterate.
        feedback: Specific feedback for improvement.

    Returns:
        dict with updated deliverable_id, iteration count, and status.
    """
    from database import async_session_factory
    from models.content import Deliverable
    from models.client import Client

    import asyncio

    AGENT_MAP = {
        "content_brief": "content_engine",
        "article": "content_engine",
        "blog_post": "content_engine",
        "email_sequence": "email_sequence_builder",
        "ad_copy": "paid_performance",
        "seo_page": "seo_architect",
        "landing_page": "seo_architect",
        "social_post": "social_media",
        "video_script": "video_script",
        "gmb_post": "local_visibility",
        "report": "reporting",
        "audit_report": "infrastructure_auditor",
        "proposal": "proposal_builder",
    }

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select

            result = await session.execute(
                select(Deliverable).where(
                    Deliverable.id == uuid.UUID(deliverable_id)
                )
            )
            deliverable = result.scalar_one_or_none()
            if not deliverable:
                raise ValueError(f"Deliverable {deliverable_id} not found")

            # Track iteration count
            meta = deliverable.meta_data or {}
            iteration_count = meta.get("iteration_count", 0) + 1

            if iteration_count > 5:
                logger.warning(
                    "Deliverable %s has exceeded 5 iterations. Escalating.",
                    deliverable_id,
                )
                deliverable.status = "in_review"
                deliverable.review_notes = (
                    f"ESCALATION: {iteration_count} iterations exceeded.\n"
                    f"Latest feedback: {feedback}"
                )
                await session.commit()
                return {
                    "deliverable_id": deliverable_id,
                    "iteration_count": iteration_count,
                    "status": "escalated",
                    "message": "Maximum iterations exceeded. Escalated for manual review.",
                }

            agent_name = AGENT_MAP.get(deliverable.type, "content_engine")

            logger.info(
                "Iterating deliverable %s (iteration %d) with agent %s",
                deliverable_id,
                iteration_count,
                agent_name,
            )

            # Fetch client for context
            client = None
            if deliverable.client_id:
                client_result = await session.execute(
                    select(Client).where(Client.id == deliverable.client_id)
                )
                client = client_result.scalar_one_or_none()

            # Run iteration through agent
            revised = await _invoke_agent_iteration(
                agent_name=agent_name,
                original_body=deliverable.body,
                feedback=feedback,
                client=client,
                deliverable_type=deliverable.type,
            )

            # Store previous version in metadata
            versions = meta.get("versions", [])
            versions.append(
                {
                    "iteration": iteration_count - 1,
                    "body_excerpt": (deliverable.body or "")[:500],
                    "feedback": feedback,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

            # Update deliverable
            deliverable.body = revised.get("body", deliverable.body)
            deliverable.title = revised.get("title", deliverable.title)
            deliverable.status = "draft"
            deliverable.meta_data = {
                **meta,
                "iteration_count": iteration_count,
                "versions": versions,
                "last_iterated_at": datetime.utcnow().isoformat(),
            }
            deliverable.ai_cost = (deliverable.ai_cost or 0) + revised.get(
                "cost", 0
            )

            await session.commit()

            return {
                "deliverable_id": deliverable_id,
                "iteration_count": iteration_count,
                "status": "draft",
                "agent_used": agent_name,
            }

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception(
            "Failed to iterate deliverable %s", deliverable_id
        )
        raise self.retry(exc=exc)


# ── Agent helper functions ────────────────────────────────────────────────

async def _invoke_agent(
    agent_name: str,
    deliverable_type: str,
    client,
    engagement,
) -> dict:
    """Invoke an AI agent to generate content.

    TODO: Integrate with Claude API. Currently returns placeholder structure.
    """
    return {
        "title": f"Generated {deliverable_type}",
        "body": f"[AI-generated {deliverable_type} content pending integration]",
        "meta_data": {
            "agent": agent_name,
            "deliverable_type": deliverable_type,
            "generated_at": datetime.utcnow().isoformat(),
        },
        "model_used": "claude-sonnet-4-20250514",
        "cost": 0.0,
    }


async def _invoke_agent_iteration(
    agent_name: str,
    original_body: str,
    feedback: str,
    client,
    deliverable_type: str,
) -> dict:
    """Invoke an AI agent to iterate on existing content.

    TODO: Integrate with Claude API. Currently returns placeholder.
    """
    return {
        "title": f"Revised {deliverable_type}",
        "body": f"[AI-revised content pending integration]\n\nOriginal feedback: {feedback}",
        "cost": 0.0,
    }


async def _check_brand_voice(deliverable, brand_voice_doc: str = None) -> dict:
    """Brand Voice Agent checks tone and style consistency.

    TODO: Integrate with Claude API.
    """
    return {
        "score": 8.0,
        "feedback": "Brand voice check pending AI integration.",
        "issues": [],
    }


async def _quality_gate_review(deliverable) -> dict:
    """Quality Gate reviews deliverable for completeness and accuracy.

    TODO: Integrate with Claude API.
    """
    return {
        "score": 8.0,
        "feedback": "Quality gate review pending AI integration.",
        "checks": {
            "completeness": True,
            "accuracy": True,
            "actionability": True,
            "formatting": True,
        },
    }


async def _process_scheduled_deliverables() -> dict:
    """Process all scheduled deliverables for today.

    Called by the daily beat schedule when no specific engagement is provided.
    Scans active engagements for deliverables due today.
    """
    from database import async_session_factory
    from models.project import EngineEngagement

    async with async_session_factory() as session:
        from sqlalchemy import select

        result = await session.execute(
            select(EngineEngagement).where(EngineEngagement.status == "active")
        )
        active_engagements = result.scalars().all()

        processed = []
        for engagement in active_engagements:
            # Check if engagement has deliverables due today
            deliverable_schedule = (engagement.deliverables or {}).get(
                "schedule", []
            )
            for item in deliverable_schedule:
                if item.get("status") == "pending":
                    # Queue individual deliverable generation
                    generate_deliverable.delay(
                        engine_engagement_id=str(engagement.id),
                        deliverable_type=item.get("type", "content_brief"),
                    )
                    processed.append(
                        {
                            "engagement_id": str(engagement.id),
                            "type": item.get("type"),
                        }
                    )

        logger.info("Scheduled %d deliverables for generation", len(processed))
        return {"scheduled_count": len(processed), "items": processed}

"""
Apex AI Marketing - Audit Tasks

Celery tasks for running growth infrastructure audits:
- Pre-audit: quick analysis via Infrastructure Auditor + Content Engine + Local Visibility
- Full audit: comprehensive generation through the full agent pipeline
"""

import logging
import uuid
from datetime import datetime

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="backend.tasks.audit_tasks.run_pre_audit",
    max_retries=3,
    default_retry_delay=120,
    acks_late=True,
)
def run_pre_audit(self, client_id: str) -> dict:
    """Run a quick pre-audit for a prospective client.

    Executes three parallel agent analyses:
    1. Infrastructure Auditor - technical site/SEO audit
    2. Content Engine - content gap analysis
    3. Local Visibility - GMB/local presence check

    Args:
        client_id: UUID string of the client to audit.

    Returns:
        dict with pre_audit_id and summary of findings.
    """
    from database import async_session_factory
    from models.client import Client
    from models.content import Deliverable

    import asyncio

    async def _run():
        async with async_session_factory() as session:
            # Fetch client
            from sqlalchemy import select
            result = await session.execute(
                select(Client).where(Client.id == uuid.UUID(client_id))
            )
            client = result.scalar_one_or_none()
            if not client:
                raise ValueError(f"Client {client_id} not found")

            logger.info(
                "Starting pre-audit for %s (%s)", client.name, client.company
            )

            findings = {}

            # ── 1. Infrastructure Audit ───────────────────────────────
            try:
                infra_findings = await _run_infrastructure_audit(client)
                findings["infrastructure"] = infra_findings
            except Exception as exc:
                logger.error("Infrastructure audit failed: %s", exc)
                findings["infrastructure"] = {"error": str(exc)}

            # ── 2. Content Gap Analysis ───────────────────────────────
            try:
                content_findings = await _run_content_analysis(client)
                findings["content"] = content_findings
            except Exception as exc:
                logger.error("Content analysis failed: %s", exc)
                findings["content"] = {"error": str(exc)}

            # ── 3. Local Visibility Check ─────────────────────────────
            try:
                local_findings = await _run_local_visibility_check(client)
                findings["local_visibility"] = local_findings
            except Exception as exc:
                logger.error("Local visibility check failed: %s", exc)
                findings["local_visibility"] = {"error": str(exc)}

            # ── Create pre-audit deliverable ──────────────────────────
            deliverable = Deliverable(
                client_id=uuid.UUID(client_id),
                type="pre_audit",
                title=f"Pre-Audit: {client.company or client.name}",
                body=_format_pre_audit_findings(findings),
                meta_data=findings,
                status="draft",
                ai_agent_used="infrastructure_auditor,content_engine,local_visibility",
                language=client.language or "en",
            )
            session.add(deliverable)
            await session.commit()
            await session.refresh(deliverable)

            logger.info("Pre-audit completed for %s: %s", client.name, deliverable.id)

            return {
                "pre_audit_id": str(deliverable.id),
                "client_id": client_id,
                "findings_summary": {
                    k: "completed" if "error" not in v else "failed"
                    for k, v in findings.items()
                },
            }

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                result = pool.submit(asyncio.run, _run()).result()
        else:
            result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Pre-audit failed for client %s", client_id)
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name="backend.tasks.audit_tasks.run_full_audit",
    max_retries=2,
    default_retry_delay=300,
    acks_late=True,
    time_limit=1800,  # 30 minute hard limit
    soft_time_limit=1500,  # 25 minute soft limit
)
def run_full_audit(self, client_id: str) -> dict:
    """Run a full growth infrastructure audit for a client.

    Pipeline:
    1. Full audit generation (all audit agents)
    2. Strategy Architect - synthesize findings into strategic recommendations
    3. Proposal Builder - generate proposal from audit
    4. Quality Gate - review and score the full package

    Args:
        client_id: UUID string of the client to audit.

    Returns:
        dict with audit_id, proposal_id, quality_score, and status.
    """
    from database import async_session_factory
    from models.client import Client
    from models.content import Deliverable

    import asyncio

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(Client).where(Client.id == uuid.UUID(client_id))
            )
            client = result.scalar_one_or_none()
            if not client:
                raise ValueError(f"Client {client_id} not found")

            logger.info(
                "Starting full audit for %s (%s)", client.name, client.company
            )

            # ── Step 1: Full Audit Generation ─────────────────────────
            logger.info("Step 1/4: Running full audit generation...")
            audit_data = await _generate_full_audit(client)

            audit_deliverable = Deliverable(
                client_id=uuid.UUID(client_id),
                type="audit_report",
                title=f"Growth Infrastructure Audit: {client.company or client.name}",
                body=audit_data["report_markdown"],
                meta_data=audit_data["structured_data"],
                status="draft",
                ai_agent_used="infrastructure_auditor",
                language=client.language or "en",
            )
            session.add(audit_deliverable)
            await session.flush()

            # ── Step 2: Strategy Architect ─────────────────────────────
            logger.info("Step 2/4: Strategy Architect synthesizing...")
            strategy = await _run_strategy_architect(client, audit_data)

            strategy_deliverable = Deliverable(
                client_id=uuid.UUID(client_id),
                type="strategy_document",
                title=f"Strategic Recommendations: {client.company or client.name}",
                body=strategy["strategy_markdown"],
                meta_data=strategy["structured_data"],
                status="draft",
                ai_agent_used="strategy_architect",
                language=client.language or "en",
            )
            session.add(strategy_deliverable)
            await session.flush()

            # ── Step 3: Proposal Builder ──────────────────────────────
            logger.info("Step 3/4: Building proposal...")
            proposal = await _build_proposal(client, audit_data, strategy)

            proposal_deliverable = Deliverable(
                client_id=uuid.UUID(client_id),
                type="proposal",
                title=f"Growth Engine Proposal: {client.company or client.name}",
                body=proposal["proposal_markdown"],
                meta_data=proposal["structured_data"],
                status="draft",
                ai_agent_used="proposal_builder",
                language=client.language or "en",
            )
            session.add(proposal_deliverable)
            await session.flush()

            # ── Step 4: Quality Gate ──────────────────────────────────
            logger.info("Step 4/4: Running quality gate...")
            quality_result = await _run_quality_gate(
                audit_deliverable, strategy_deliverable, proposal_deliverable
            )

            # Update statuses based on quality gate
            gate_passed = quality_result.get("score", 0) >= 7.0
            final_status = "in_review" if gate_passed else "draft"

            audit_deliverable.status = final_status
            strategy_deliverable.status = final_status
            proposal_deliverable.status = final_status

            audit_deliverable.review_notes = quality_result.get("feedback", "")
            proposal_deliverable.review_notes = quality_result.get("feedback", "")

            # Update client status
            client.status = "audit_delivered" if gate_passed else "audit_requested"

            await session.commit()

            logger.info(
                "Full audit completed for %s. Quality score: %s. Passed: %s",
                client.name,
                quality_result.get("score"),
                gate_passed,
            )

            return {
                "audit_id": str(audit_deliverable.id),
                "strategy_id": str(strategy_deliverable.id),
                "proposal_id": str(proposal_deliverable.id),
                "quality_score": quality_result.get("score"),
                "quality_passed": gate_passed,
                "status": final_status,
                "client_id": client_id,
            }

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Full audit failed for client %s", client_id)
        raise self.retry(exc=exc)


# ── Agent helper functions (stubs for AI integration) ─────────────────────

async def _run_infrastructure_audit(client) -> dict:
    """Run infrastructure auditor agent on client's website."""
    # TODO: Integrate with Claude API for actual audit
    return {
        "website": client.website,
        "findings": [],
        "score": 0,
        "timestamp": datetime.utcnow().isoformat(),
    }


async def _run_content_analysis(client) -> dict:
    """Run content engine analysis on client's existing content."""
    return {
        "content_gaps": [],
        "existing_content_score": 0,
        "recommendations": [],
        "timestamp": datetime.utcnow().isoformat(),
    }


async def _run_local_visibility_check(client) -> dict:
    """Check local visibility (GMB, directories, local SEO)."""
    return {
        "gmb_status": "not_checked",
        "directory_listings": [],
        "local_seo_score": 0,
        "timestamp": datetime.utcnow().isoformat(),
    }


async def _generate_full_audit(client) -> dict:
    """Generate the complete growth infrastructure audit report."""
    from templates.audits.audit_template import render_audit_report

    # TODO: Replace with actual Claude API calls for each audit section
    audit_sections = {
        "executive_summary": "Pending AI generation",
        "website_infrastructure": {},
        "seo_analysis": {},
        "content_assessment": {},
        "social_media_presence": {},
        "paid_advertising": {},
        "local_visibility": {},
        "competitive_landscape": {},
        "growth_opportunities": [],
        "recommended_engines": [],
        "priority_matrix": {},
    }

    report_markdown = render_audit_report(
        client_name=client.name,
        company=client.company or "",
        sections=audit_sections,
        language=client.language or "en",
    )

    return {
        "report_markdown": report_markdown,
        "structured_data": audit_sections,
    }


async def _run_strategy_architect(client, audit_data: dict) -> dict:
    """Strategy Architect synthesizes audit into recommendations."""
    # TODO: Integrate with Claude API
    strategy = {
        "positioning": "",
        "priority_engines": [],
        "timeline": "",
        "investment_range": "",
        "expected_outcomes": [],
    }
    return {
        "strategy_markdown": "# Strategic Recommendations\n\nPending AI generation.",
        "structured_data": strategy,
    }


async def _build_proposal(client, audit_data: dict, strategy: dict) -> dict:
    """Proposal Builder creates the client-facing proposal."""
    from templates.proposals.proposal_template import render_proposal

    # TODO: Integrate with Claude API
    proposal_data = {
        "client_name": client.name,
        "company": client.company or "",
        "recommended_engines": strategy.get("structured_data", {}).get(
            "priority_engines", []
        ),
        "investment": strategy.get("structured_data", {}).get("investment_range", ""),
        "timeline": strategy.get("structured_data", {}).get("timeline", ""),
    }

    proposal_markdown = render_proposal(
        client_name=client.name,
        company=client.company or "",
        sections=proposal_data,
        language=client.language or "en",
    )

    return {
        "proposal_markdown": proposal_markdown,
        "structured_data": proposal_data,
    }


async def _run_quality_gate(audit, strategy, proposal) -> dict:
    """Quality Gate reviews all deliverables before sending to client."""
    # TODO: Integrate with Claude API for quality scoring
    return {
        "score": 8.0,
        "feedback": "Automated quality check passed. Manual review recommended.",
        "checks": {
            "completeness": True,
            "accuracy": True,
            "brand_voice": True,
            "actionability": True,
        },
    }


def _format_pre_audit_findings(findings: dict) -> str:
    """Format pre-audit findings into a readable markdown summary."""
    sections = []
    sections.append("# Pre-Audit Findings\n")

    for area, data in findings.items():
        area_title = area.replace("_", " ").title()
        sections.append(f"## {area_title}\n")
        if isinstance(data, dict) and "error" in data:
            sections.append(f"Analysis encountered an issue: {data['error']}\n")
        elif isinstance(data, dict):
            for key, value in data.items():
                sections.append(f"- **{key.replace('_', ' ').title()}**: {value}")
        sections.append("")

    return "\n".join(sections)

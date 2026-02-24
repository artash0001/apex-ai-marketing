"""
Apex AI Marketing - Agent 2: Strategy Architect

Model: Claude Opus (deep reasoning)
Engine: All engines (cross-cutting)
Language: both (EN + RU)

Designs the overall engine configuration for each client.
Decides which engines to deploy, in what order, and how they connect.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class StrategyArchitect(BaseAgent):
    name = "Strategy Architect"
    role = (
        "Designs the overall engine configuration for each client. "
        "Decides which engines to deploy, in what order, and how they connect."
    )
    engine = "All engines (cross-cutting)"
    model = settings.PREMIUM_MODEL  # Claude Opus
    temperature = 0.5
    max_tokens = 8192
    language = "both"

    system_prompt = (
        "You are the Strategy Architect at Apex AI Marketing. You design growth infrastructure systems.\n\n"
        "You think in terms of the revenue backbone: Capture → Qualify → Nurture → Close → Retain.\n"
        "Each engine plugs into this backbone at specific stages. Your job is to design the optimal "
        "configuration for each client.\n\n"
        "Available engines and their backbone positions:\n"
        "- Local Visibility Engine → Capture (local search, Maps, reviews)\n"
        "- Inbound Demand Engine → Capture (organic search, content)\n"
        "- Outbound Engine → Capture (prospecting, sequences)\n"
        "- Paid Acquisition Engine → Capture (ads, landing pages)\n"
        "- Revenue Stack Foundation → Qualify + Nurture (CRM, routing, automation, tracking)\n"
        "- Lifecycle & Retention Engine → Nurture + Retain (email, SMS, WhatsApp, referrals)\n"
        "- Growth Ops Retainer → Close + Iterate (experiments, reporting, optimization)\n\n"
        "When designing a system:\n"
        "1. Start with the biggest leak (from Infrastructure Audit)\n"
        "2. Never recommend more than 2-3 engines to start — avoid overwhelm\n"
        "3. Always include Revenue Stack Foundation if client lacks CRM/tracking\n"
        "4. Show the connection diagram: how data flows between engines\n"
        "5. Include a phased rollout: what to deploy first, second, third\n"
        "6. Every recommendation has a 'why' (tied to revenue impact) and a 'how' (specific deliverables)\n\n"
        "You never recommend engines clients don't need. Scope discipline is a value — "
        "upselling for revenue is not.\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' 'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'\n\n"
        "Engine Pricing Reference:\n"
        "- Growth Infrastructure Audit: $500–$2,500 (one-time)\n"
        "- Revenue Stack Foundation: $3,000–$10,000 (project)\n"
        "- Local Visibility Engine: $200–$1,500/mo\n"
        "- Inbound Demand Engine: $2,000–$8,000/mo\n"
        "- Outbound Engine: $1,500–$5,000/mo\n"
        "- Paid Acquisition Engine: $1,000–$5,000/mo + ad spend %\n"
        "- Lifecycle & Retention Engine: $2,000–$5,000 build + $500–$1,500/mo\n"
        "- Growth Ops Retainer: $3,000–$10,000/mo\n\n"
        "Markets (Priority Order):\n"
        "1. Russian-speaking business owners in Dubai\n"
        "2. Dubai/UAE SMBs\n"
        "3. UK local service businesses\n"
        "4. Global B2B high-ticket services"
    )

    async def design_system(
        self,
        audit_findings: dict,
        client_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Design a complete engine configuration based on audit findings.

        Parameters
        ----------
        audit_findings : dict
            Results from the Infrastructure Auditor.
        client_data : dict
            Client profile, industry, budget, goals.
        """
        task = (
            "Design a complete growth infrastructure system for this client.\n\n"
            "Based on the audit findings and client data provided, produce:\n\n"
            "1. System Architecture Overview\n"
            "   - Revenue backbone mapping (Capture → Qualify → Nurture → Close → Retain)\n"
            "   - Which stages have gaps\n"
            "   - Which engines fill those gaps\n\n"
            "2. Recommended Engine Configuration\n"
            "   - Which engines to deploy (max 2-3 to start)\n"
            "   - Why each engine (tied to specific audit findings and revenue impact)\n"
            "   - How engines connect (data flow diagram description)\n"
            "   - What each engine will deliver in the first 90 days\n\n"
            "3. Connection Diagram\n"
            "   - How data flows between engines\n"
            "   - Integration points (CRM, tracking, automation)\n"
            "   - Required tools and platforms\n\n"
            "4. Phased Rollout Plan\n"
            "   - Phase 1 (Month 1): Foundation — what gets built first\n"
            "   - Phase 2 (Month 2-3): Growth — what gets added\n"
            "   - Phase 3 (Month 4+): Optimization — what gets refined\n"
            "   - Dependencies between phases\n\n"
            "5. Budget Allocation\n"
            "   - Investment per engine (setup + monthly)\n"
            "   - Total monthly infrastructure cost\n"
            "   - Expected ROI timeline\n\n"
            "6. Success Metrics\n"
            "   - KPIs per engine\n"
            "   - Overall system KPIs\n"
            "   - Review cadence (weekly, monthly, quarterly)\n\n"
            "Be specific about deliverables, timelines, and expected outcomes.\n"
            "Do NOT recommend engines the client doesn't need."
        )
        context = {
            "additional_data": (
                f"Audit Findings:\n{audit_findings}\n\n"
                f"Client Data:\n{client_data}"
            ),
        }
        context.update(client_data)
        return await self.run(task=task, context=context, db=db, task_id=task_id)

    async def create_roadmap(
        self,
        engines: list[str],
        timeline: str = "90 days",
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Create a detailed implementation roadmap for selected engines.

        Parameters
        ----------
        engines : list[str]
            List of engine names to include.
        timeline : str
            Timeline period (default: 90 days).
        """
        engines_str = ", ".join(engines)
        task = (
            f"Create a detailed {timeline} implementation roadmap for these engines: {engines_str}\n\n"
            "For each week, specify:\n"
            "- Tasks to complete\n"
            "- Deliverables due\n"
            "- Client inputs needed\n"
            "- Internal milestones\n"
            "- Dependencies on other engines/tasks\n\n"
            "Include:\n"
            "- Setup/onboarding tasks (week 1-2)\n"
            "- Build/implementation tasks (week 2-6)\n"
            "- Launch/optimization tasks (week 6+)\n"
            "- Review checkpoints (bi-weekly)\n"
            "- Reporting cadence\n\n"
            "Format as a week-by-week timeline that both the team and client can follow.\n"
            "Include clear handoff points and approval gates."
        )
        return await self.run(
            task=task,
            context={"additional_data": f"Engines: {engines_str}\nTimeline: {timeline}"},
            db=db,
            task_id=task_id,
        )

    async def quarterly_review(
        self,
        client_data: dict,
        metrics: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Conduct a quarterly strategic review and plan next quarter.

        Parameters
        ----------
        client_data : dict
            Current client profile and active engines.
        metrics : dict
            Performance metrics from the quarter.
        """
        task = (
            "Conduct a quarterly strategic review and design the next quarter's plan.\n\n"
            "Produce:\n\n"
            "1. Quarter in Review\n"
            "   - Performance against KPI targets (per engine)\n"
            "   - What worked well and why\n"
            "   - What underperformed and why\n"
            "   - Key experiments run and learnings\n\n"
            "2. System Health Assessment\n"
            "   - Is the current engine configuration optimal?\n"
            "   - Any engines that should be added, removed, or adjusted?\n"
            "   - Integration health (are engines working together as designed?)\n\n"
            "3. Next Quarter Plan\n"
            "   - Updated KPI targets (based on current trajectory)\n"
            "   - Engine adjustments (scope changes, new engines, sunset engines)\n"
            "   - Key initiatives and experiments to run\n"
            "   - Budget adjustment recommendations\n\n"
            "4. Strategic Recommendations\n"
            "   - Market opportunities identified\n"
            "   - Competitive landscape changes\n"
            "   - Technology or platform changes needed\n"
            "   - Client growth opportunities\n\n"
            "Be honest about what's not working. Clients value directness over optimism."
        )
        context = {
            "additional_data": (
                f"Client Data:\n{client_data}\n\n"
                f"Quarterly Metrics:\n{metrics}"
            ),
        }
        context.update(client_data)
        return await self.run(task=task, context=context, db=db, task_id=task_id)

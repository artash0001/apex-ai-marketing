"""
Apex AI Marketing - Agent 1: Infrastructure Auditor

Model: Claude Opus (complex analysis)
Engine: Growth Infrastructure Audit
Language: both (EN + RU)

Diagnoses funnels, tracking gaps, and revenue leaks.
Produces the Growth Infrastructure Audit.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class InfrastructureAuditor(BaseAgent):
    name = "Infrastructure Auditor"
    role = "Diagnoses funnels, tracking gaps, and revenue leaks. Produces the Growth Infrastructure Audit."
    engine = "Growth Infrastructure Audit"
    model = settings.PREMIUM_MODEL  # Claude Opus
    temperature = 0.4
    max_tokens = 8192
    language = "both"

    system_prompt = (
        "You are the Infrastructure Auditor at Apex AI Marketing, an AI Growth Infrastructure agency.\n\n"
        "Your job is to diagnose where revenue leaks exist in a business's marketing infrastructure. "
        "You think in systems: capture → qualify → nurture → close → retain — with measurement at every stage.\n\n"
        "When given a client's business info, website, and analytics access, you produce:\n"
        "1. Tracking & Attribution Map (what is measured, what is missing, what is broken)\n"
        "2. Funnel Teardown (conversion rates per stage, benchmarked against industry)\n"
        "3. Competitive Scan (3-5 direct competitors — their channels, positioning, gaps)\n"
        "4. Revenue Leak Identification (specific points where leads/money are lost)\n"
        "5. 90-Day Build Plan (prioritized engine recommendations with expected impact)\n"
        "6. KPI Targets (baseline metrics + target metrics with timelines)\n\n"
        "Rules:\n"
        "- NEVER fabricate data. If you don't have real analytics, say 'requires access to verify'\n"
        "- Every recommendation must specify which engine solves it\n"
        "- Prioritize by expected revenue impact, not by what's easiest\n"
        "- Be direct about what's broken. Clients hire us because agencies before us were vague.\n"
        "- Frame findings as system problems, not people problems\n"
        "- Include estimated timeline and required client inputs for each recommendation\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' 'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'\n\n"
        "Available Engines for Recommendations:\n"
        "- Revenue Stack Foundation ($3,000–$10,000 project): CRM, automation, tracking, dashboards\n"
        "- Local Visibility Engine ($200–$1,500/mo): GBP, citations, reviews, local content\n"
        "- Inbound Demand Engine ($2,000–$8,000/mo): Topic maps, content, SEO, GEO/AEO\n"
        "- Outbound Engine ($1,500–$5,000/mo): Cold outreach, sequences, prospecting\n"
        "- Paid Acquisition Engine ($1,000–$5,000/mo + ad spend): Ads, landing pages, A/B tests\n"
        "- Lifecycle & Retention Engine ($2,000–$5,000 build + $500–$1,500/mo): Email/SMS/WhatsApp flows\n"
        "- Growth Ops Retainer ($3,000–$10,000/mo): Experiments, reporting, optimization"
    )

    async def run_full_audit(
        self,
        client_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Run a complete Growth Infrastructure Audit for a client.

        Parameters
        ----------
        client_data : dict
            Client info, website URL, analytics data, industry, competitors.
        db : AsyncSession, optional
            Database session for cost tracking.
        task_id : str, optional
            Link usage to a specific Task record.

        Returns
        -------
        AgentOutput
            The complete audit report.
        """
        task = (
            "Perform a complete Growth Infrastructure Audit for the following client.\n\n"
            "Produce ALL 6 sections:\n"
            "1. Tracking & Attribution Map\n"
            "2. Funnel Teardown\n"
            "3. Competitive Scan (analyze 3-5 competitors)\n"
            "4. Revenue Leak Identification\n"
            "5. 90-Day Build Plan (with engine recommendations)\n"
            "6. KPI Targets (baseline + targets)\n\n"
            "Format as a professional deliverable document with clear sections, "
            "tables where appropriate, and actionable recommendations tied to specific engines."
        )
        return await self.run(task=task, context=client_data, db=db, task_id=task_id)

    async def run_pre_audit(
        self,
        website_url: str,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Run a lightweight pre-audit based on publicly available information.

        Used for sales conversations before full engagement.

        Parameters
        ----------
        website_url : str
            The prospect's website URL.
        """
        task = (
            f"Perform a quick pre-audit scan of this business based on their website: {website_url}\n\n"
            "This is a sales tool — we're showing the prospect we can identify issues before they hire us.\n\n"
            "Produce:\n"
            "1. First Impressions (what stands out, good and bad)\n"
            "2. Obvious Gaps (tracking, conversion paths, mobile experience, speed)\n"
            "3. Quick Win Opportunities (3-5 things that could improve within 30 days)\n"
            "4. Recommended Next Step (which full audit or engine engagement makes sense)\n\n"
            "Keep it concise (1-2 pages). Be specific enough to demonstrate expertise, "
            "but leave enough depth for the full paid audit.\n\n"
            "Important: Only assess what's publicly visible. Mark anything that requires "
            "analytics access as 'requires access to verify.'"
        )
        return await self.run(
            task=task,
            context={"website_url": website_url},
            db=db,
            task_id=task_id,
        )

    async def generate_tracking_map(
        self,
        analytics_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate a detailed tracking and attribution map.

        Parameters
        ----------
        analytics_data : dict
            Current tracking setup, tools in use, events tracked, goals.
        """
        task = (
            "Generate a comprehensive Tracking & Attribution Map.\n\n"
            "Produce:\n"
            "1. Current State Assessment\n"
            "   - What tools are installed (GA4, GTM, pixels, etc.)\n"
            "   - What events are being tracked\n"
            "   - What conversion goals are configured\n"
            "   - Current attribution model in use\n\n"
            "2. Gap Analysis\n"
            "   - Missing tracking points (form submissions, phone calls, chat, etc.)\n"
            "   - Broken or misconfigured tracking\n"
            "   - Missing cross-domain tracking\n"
            "   - Missing UTM conventions\n\n"
            "3. Recommended Tracking Architecture\n"
            "   - Event taxonomy (naming convention for all events)\n"
            "   - Conversion event hierarchy (micro → macro conversions)\n"
            "   - UTM convention document\n"
            "   - Attribution model recommendation (with rationale)\n"
            "   - Dashboard requirements (what metrics to display where)\n\n"
            "4. Implementation Checklist\n"
            "   - Prioritized list of tracking fixes\n"
            "   - Tools needed\n"
            "   - Estimated implementation time\n"
            "   - Required access and permissions\n\n"
            "Format as a technical implementation document that a developer or CRM admin can follow."
        )
        return await self.run(task=task, context=analytics_data, db=db, task_id=task_id)

"""
Apex AI Marketing - Agent 9: Analytics Engineer

Model: Claude Sonnet
Engine: Growth Ops Retainer + all engines (reporting)
Language: both (EN + RU)

Creates performance reports, dashboards, KPI tracking,
and data-driven recommendations.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class AnalyticsEngineer(BaseAgent):
    name = "Analytics Engineer"
    role = (
        "Creates performance reports, dashboards, KPI tracking, "
        "and data-driven recommendations."
    )
    engine = "Growth Ops Retainer + all engines (reporting)"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.4  # Low temp for data accuracy
    max_tokens = 6144
    language = "both"

    system_prompt = (
        "You turn marketing data into actionable decisions. You don't create data dumps — "
        "you create insight documents.\n\n"
        "Report structure:\n"
        "1. Executive Summary (3 bullets: what happened, why it matters, what to do next)\n"
        "2. North-Star KPI Status (vs target, vs previous period)\n"
        "3. Engine Performance (metrics per active engine)\n"
        "4. What Worked (top 3 wins with data and why)\n"
        "5. What Didn't (top 3 underperformers with diagnosis)\n"
        "6. Experiment Results (what was tested, what was learned, what decision was made)\n"
        "7. Recommendations (specific, actionable, prioritized by expected revenue impact)\n"
        "8. Next Period Focus (3 priorities)\n\n"
        "Rules:\n"
        "- Lead with insights, not data\n"
        "- Always compare to: previous period, target, and industry benchmark\n"
        "- Use plain language — clients are business owners, not analysts\n"
        "- Every insight must have a 'so what' and a 'now what'\n"
        "- Include specific action items with owners and deadlines\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' "
        "'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'\n\n"
        "Data Integrity Rules:\n"
        "- NEVER fabricate metrics or make up data points\n"
        "- If data is missing, say 'data not available' and explain what's needed to get it\n"
        "- Distinguish between: verified data, projected data, and industry benchmarks\n"
        "- Always cite the data source (GA4, CRM, ad platform, etc.)\n"
        "- Flag any data quality issues (incomplete tracking, attribution gaps)\n\n"
        "Visualization Recommendations:\n"
        "- Use appropriate chart types (trend = line, comparison = bar, proportion = pie)\n"
        "- Always include period-over-period comparison\n"
        "- Highlight targets with reference lines\n"
        "- Red/yellow/green status indicators for KPIs"
    )

    async def generate_weekly_report(
        self,
        client_data: dict,
        metrics: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate a weekly performance report.

        Parameters
        ----------
        client_data : dict
            Client profile, active engines, KPI targets.
        metrics : dict
            This week's performance metrics across all channels.
        """
        task = (
            "Generate a weekly performance report for this client.\n\n"
            "Report structure:\n\n"
            "1. Executive Summary (3 bullets max)\n"
            "   - Most important thing that happened this week\n"
            "   - Why it matters to the business\n"
            "   - What to do about it\n\n"
            "2. KPI Dashboard\n"
            "   For each North-Star KPI:\n"
            "   - Current value\n"
            "   - vs. target (% to goal)\n"
            "   - vs. last week (trend direction + %)\n"
            "   - Status: On Track / At Risk / Off Track\n\n"
            "3. Engine Performance Summary\n"
            "   For each active engine:\n"
            "   - Key metric(s) this week\n"
            "   - Notable changes or trends\n"
            "   - Actions taken this week\n\n"
            "4. Quick Wins & Alerts\n"
            "   - Top 2 wins this week (with data)\n"
            "   - Top 2 concerns (with data)\n"
            "   - Any urgent actions needed\n\n"
            "5. Next Week Focus\n"
            "   - Top 3 priorities\n"
            "   - Experiments to run/review\n"
            "   - Client input needed (if any)\n\n"
            "Keep it concise — this should be scannable in 3 minutes.\n"
            "Use tables for metrics, not paragraphs.\n"
            "If data is missing for any metric, flag it clearly."
        )
        context = {
            "additional_data": (
                f"Client Data:\n{client_data}\n\n"
                f"This Week's Metrics:\n{metrics}"
            ),
        }
        context.update(client_data)
        return await self.run(task=task, context=context, db=db, task_id=task_id)

    async def generate_monthly_report(
        self,
        client_data: dict,
        metrics: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate a comprehensive monthly performance report.

        Parameters
        ----------
        client_data : dict
            Client profile, active engines, KPI targets.
        metrics : dict
            Monthly performance metrics, experiment results, costs.
        """
        task = (
            "Generate a comprehensive monthly performance report.\n\n"
            "Full report structure:\n\n"
            "1. Executive Summary (3-5 bullets)\n"
            "   - What happened this month (key events and results)\n"
            "   - Why it matters (business impact)\n"
            "   - What to do next (top 3 actions)\n\n"
            "2. North-Star KPI Status\n"
            "   - Current value vs. target\n"
            "   - vs. previous month\n"
            "   - vs. same month last year (if available)\n"
            "   - Trend analysis and forecast\n\n"
            "3. Engine Performance (detailed per engine)\n"
            "   For each active engine:\n"
            "   - All relevant metrics\n"
            "   - vs. targets\n"
            "   - vs. previous month\n"
            "   - Key activities and deliverables completed\n"
            "   - Issues encountered and how they were resolved\n\n"
            "4. What Worked (top 3 wins)\n"
            "   - What happened\n"
            "   - Data to prove it\n"
            "   - Why it worked\n"
            "   - How to replicate/scale it\n\n"
            "5. What Didn't Work (top 3 underperformers)\n"
            "   - What happened\n"
            "   - Data showing the gap\n"
            "   - Diagnosis (why it didn't work)\n"
            "   - Corrective action plan\n\n"
            "6. Experiment Results\n"
            "   For each experiment run:\n"
            "   - Hypothesis, variable changed, result\n"
            "   - Decision (implement, iterate, discard)\n"
            "   - Learning captured\n\n"
            "7. Cost & ROI Analysis\n"
            "   - Total investment this month (tools, ad spend, services)\n"
            "   - Revenue attributed to marketing\n"
            "   - Cost per lead, cost per acquisition\n"
            "   - ROI calculation (if data available)\n\n"
            "8. Recommendations (prioritized)\n"
            "   - What to start doing\n"
            "   - What to stop doing\n"
            "   - What to continue doing\n"
            "   - Budget reallocation suggestions\n\n"
            "9. Next Month Focus\n"
            "   - Top 3 priorities\n"
            "   - Experiments to run\n"
            "   - Deliverables scheduled\n"
            "   - Client inputs needed\n\n"
            "Use tables, charts descriptions, and visual formatting.\n"
            "This is a client-facing document — professional but accessible."
        )
        context = {
            "additional_data": (
                f"Client Data:\n{client_data}\n\n"
                f"Monthly Metrics:\n{metrics}"
            ),
        }
        context.update(client_data)
        return await self.run(task=task, context=context, db=db, task_id=task_id)

    async def create_dashboard_spec(
        self,
        client_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Create a dashboard specification document.

        Parameters
        ----------
        client_data : dict
            Client profile, active engines, KPI targets, tools in use.
        """
        task = (
            "Create a comprehensive dashboard specification document.\n\n"
            "Produce:\n\n"
            "1. Dashboard Overview\n"
            "   - Purpose and primary audience\n"
            "   - Refresh cadence (real-time, daily, weekly)\n"
            "   - Tool recommendation (Looker Studio, Databox, custom)\n\n"
            "2. Executive Dashboard (for client)\n"
            "   - North-Star KPIs with targets\n"
            "   - Revenue pipeline status\n"
            "   - Engine health indicators (green/yellow/red)\n"
            "   - Period-over-period comparison\n"
            "   - Layout description with chart types\n\n"
            "3. Engine-Specific Dashboards\n"
            "   For each active engine:\n"
            "   - Key metrics to display\n"
            "   - Chart types and layout\n"
            "   - Filters and date ranges\n"
            "   - Drill-down capabilities\n\n"
            "4. Data Sources\n"
            "   - Which platforms feed each metric\n"
            "   - API connections needed\n"
            "   - Data transformation requirements\n"
            "   - Data freshness requirements\n\n"
            "5. Alert Conditions\n"
            "   - KPI threshold alerts (above/below target)\n"
            "   - Anomaly detection rules\n"
            "   - Notification channels (email, Telegram, Slack)\n\n"
            "6. Implementation Plan\n"
            "   - Priority order (which dashboards first)\n"
            "   - Estimated setup time\n"
            "   - Required access and permissions\n"
            "   - Testing checklist\n\n"
            "Format as a technical specification that a dashboard developer can implement."
        )
        return await self.run(task=task, context=client_data, db=db, task_id=task_id)

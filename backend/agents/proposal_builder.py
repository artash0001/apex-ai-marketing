"""
Apex AI Marketing - Agent 11: Proposal Builder

Model: Claude Opus (needs strategic depth)
Engine: All engines (sales)
Language: both (EN + RU)

Creates client proposals and SOWs for engine engagements.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class ProposalBuilder(BaseAgent):
    name = "Proposal Builder"
    role = "Creates client proposals and SOWs for engine engagements."
    engine = "All engines (sales)"
    model = settings.PREMIUM_MODEL  # Claude Opus
    temperature = 0.5
    max_tokens = 8192
    language = "both"

    system_prompt = (
        "You write proposals that close deals by showing clients exactly what they'll get, "
        "when, and what it will cost.\n\n"
        "Proposal structure:\n"
        "1. Executive Summary (their problem → our diagnosis → the engine solution → expected outcome)\n"
        "2. Infrastructure Audit Findings (what we found, where revenue leaks)\n"
        "3. Recommended Engine(s) (which engines, why, how they connect)\n"
        "4. Scope of Work (specific deliverables per engine — bulleted, concrete)\n"
        "5. What's NOT Included (scope boundaries — prevent creep)\n"
        "6. Timeline (phased, with milestones and dependencies)\n"
        "7. Investment (pricing for each engine, framed as infrastructure investment)\n"
        "8. Required Client Inputs (what we need from them — access, data, time)\n"
        "9. Success Metrics (how we'll measure if it's working)\n"
        "10. Next Steps (clear first action: sign → grant access → kickoff call)\n\n"
        "Rules:\n"
        "- Never lead with price\n"
        "- Frame everything as infrastructure investment, not marketing expense\n"
        "- Include clear inclusions AND exclusions for every engine\n"
        "- For Russian-speaking clients: produce bilingual proposals (EN + RU)\n"
        "- Make the middle tier the obvious choice if offering tiers\n"
        "- Include a 'quick-start' option for clients ready to begin immediately\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' "
        "'unlock potential'\n"
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
        "- Growth Ops Retainer: $3,000–$10,000/mo"
    )

    async def generate_proposal(
        self,
        client_data: dict,
        audit_findings: dict,
        recommended_engines: list[str],
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate a complete client proposal.

        Parameters
        ----------
        client_data : dict
            Client profile, industry, goals, budget indication.
        audit_findings : dict
            Results from the Infrastructure Auditor.
        recommended_engines : list[str]
            List of engines recommended by the Strategy Architect.
        """
        engines_str = ", ".join(recommended_engines)
        task = (
            "Generate a complete client proposal following the 10-section structure.\n\n"
            "Produce ALL 10 sections:\n\n"
            "1. Executive Summary\n"
            "   - Their problem (2-3 sentences, specific to their business)\n"
            "   - Our diagnosis (what the audit revealed)\n"
            "   - The engine solution (which engines, how they solve the problems)\n"
            "   - Expected outcome (measurable, time-bound)\n\n"
            "2. Infrastructure Audit Findings\n"
            "   - Key findings from the audit (summarized, client-friendly)\n"
            "   - Revenue leaks identified (quantified where possible)\n"
            "   - Priority ranking of issues\n\n"
            "3. Recommended Engine(s)\n"
            f"   - Engines: {engines_str}\n"
            "   - Why each engine (tied to specific findings)\n"
            "   - How they connect and create a system\n"
            "   - What each engine delivers\n\n"
            "4. Scope of Work\n"
            "   For each engine:\n"
            "   - Specific deliverables (bulleted, concrete)\n"
            "   - Activities included\n"
            "   - Monthly/weekly cadence\n\n"
            "5. What's NOT Included\n"
            "   - Clear scope boundaries per engine\n"
            "   - What would require additional engagement\n"
            "   - This prevents scope creep and sets expectations\n\n"
            "6. Timeline\n"
            "   - Phased rollout with milestones\n"
            "   - Dependencies between phases\n"
            "   - Key milestone dates\n\n"
            "7. Investment\n"
            "   - Pricing per engine (setup + monthly where applicable)\n"
            "   - Total investment summary\n"
            "   - Frame as infrastructure investment, not expense\n"
            "   - Payment terms recommendation\n\n"
            "8. Required Client Inputs\n"
            "   - Access needed (analytics, CRM, ad accounts)\n"
            "   - Data needed (customer lists, brand assets, etc.)\n"
            "   - Time commitment (approvals, calls, feedback)\n"
            "   - Timeline for providing inputs\n\n"
            "9. Success Metrics\n"
            "   - KPIs per engine with target values\n"
            "   - Measurement methodology\n"
            "   - Reporting cadence and format\n"
            "   - Review meeting schedule\n\n"
            "10. Next Steps\n"
            "    - Clear first action (sign proposal)\n"
            "    - What happens after signing (access grants, kickoff call)\n"
            "    - Timeline to first deliverable\n"
            "    - Contact info for questions\n\n"
            "Format as a professional, client-ready document.\n"
            "If client speaks Russian, include a Russian summary section."
        )
        context = {
            "additional_data": (
                f"Client Data:\n{client_data}\n\n"
                f"Audit Findings:\n{audit_findings}\n\n"
                f"Recommended Engines: {engines_str}"
            ),
        }
        context.update(client_data)
        return await self.run(task=task, context=context, db=db, task_id=task_id)

    async def generate_sow(
        self,
        proposal: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate a detailed Statement of Work from a proposal.

        Parameters
        ----------
        proposal : dict
            The approved proposal data.
        """
        task = (
            "Generate a detailed Statement of Work (SOW) based on this approved proposal.\n\n"
            "The SOW should include:\n\n"
            "1. Project Overview\n"
            "   - Client name and project name\n"
            "   - Engagement start and end dates\n"
            "   - Engagement type (project, retainer, hybrid)\n\n"
            "2. Scope of Services (per engine)\n"
            "   For each engine:\n"
            "   - Detailed deliverables list with descriptions\n"
            "   - Quantity and frequency of each deliverable\n"
            "   - Quality standards and acceptance criteria\n"
            "   - Revision policy (number of included revisions)\n\n"
            "3. Timeline and Milestones\n"
            "   - Week-by-week schedule for first 90 days\n"
            "   - Key milestones with dates\n"
            "   - Approval gates (what needs client sign-off)\n"
            "   - Dependencies and prerequisites\n\n"
            "4. Roles and Responsibilities\n"
            "   - Our team responsibilities\n"
            "   - Client responsibilities\n"
            "   - Communication protocols\n"
            "   - Escalation procedures\n\n"
            "5. Pricing and Payment Terms\n"
            "   - Line-item pricing per engine\n"
            "   - Payment schedule (monthly, milestone-based)\n"
            "   - Invoice terms (Net 15, Net 30)\n"
            "   - Late payment terms\n\n"
            "6. Success Metrics and Reporting\n"
            "   - KPIs with target values and measurement methods\n"
            "   - Reporting schedule and format\n"
            "   - Review meeting cadence\n\n"
            "7. Terms and Conditions\n"
            "   - Cancellation policy\n"
            "   - Confidentiality provisions\n"
            "   - Intellectual property ownership\n"
            "   - Limitation of liability\n\n"
            "8. Signatures\n"
            "   - Signature blocks for both parties\n"
            "   - Date fields\n\n"
            "Format as a professional legal document ready for signatures."
        )
        return await self.run(
            task=task,
            context={"additional_data": f"Approved Proposal:\n{proposal}"},
            db=db,
            task_id=task_id,
        )

    async def generate_quick_start_option(
        self,
        proposal: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate a quick-start option for clients ready to begin immediately.

        Parameters
        ----------
        proposal : dict
            The full proposal data.
        """
        task = (
            "Create a 'Quick Start' option based on this proposal.\n\n"
            "The Quick Start should:\n\n"
            "1. Identify the Highest-Impact First Step\n"
            "   - Which engine or deliverable has the most immediate impact?\n"
            "   - What can be started within 48 hours of signing?\n\n"
            "2. Quick Start Package\n"
            "   - Reduced scope: most impactful deliverables only\n"
            "   - Shorter commitment: 30-day sprint or single project\n"
            "   - Lower price point: entry-level investment\n"
            "   - Clear deliverables in 14-30 days\n\n"
            "3. Upgrade Path\n"
            "   - How the Quick Start leads to the full engagement\n"
            "   - What the client will see/learn during Quick Start\n"
            "   - Pricing for upgrading to full scope\n\n"
            "4. Quick Start Timeline\n"
            "   - Day 1-3: What happens immediately\n"
            "   - Week 1: First deliverable\n"
            "   - Week 2-4: Additional deliverables + results\n"
            "   - Week 4: Review and upgrade discussion\n\n"
            "5. Quick Start Next Steps\n"
            "   - One-page sign-off (not full SOW)\n"
            "   - Minimal client inputs needed to start\n"
            "   - First meeting agenda\n\n"
            "This is for clients who want to test the waters before committing "
            "to the full engagement. Make it easy to say yes."
        )
        return await self.run(
            task=task,
            context={"additional_data": f"Full Proposal:\n{proposal}"},
            db=db,
            task_id=task_id,
        )

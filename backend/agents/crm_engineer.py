"""
Apex AI Marketing - Agent 3: CRM Engineer

Model: Claude Sonnet
Engine: Revenue Stack Foundation
Language: en

Designs and documents CRM pipelines, automation workflows,
lead routing rules, and tracking configurations.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class CRMEngineer(BaseAgent):
    name = "CRM Engineer"
    role = (
        "Designs and documents CRM pipelines, automation workflows, "
        "lead routing rules, and tracking configurations."
    )
    engine = "Revenue Stack Foundation"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.4
    max_tokens = 6144
    language = "en"

    system_prompt = (
        "You are a CRM and marketing operations engineer. You design the systems that ensure "
        "every lead is captured, tracked, routed, and followed up — automatically.\n\n"
        "When designing a Revenue Stack Foundation, you produce:\n"
        "1. Pipeline Architecture (stages, conversion criteria, automation triggers)\n"
        "2. Lead Routing Rules (assignment logic, response time SLAs)\n"
        "3. Tracking Plan (UTM conventions, event taxonomy, conversion events)\n"
        "4. Attribution Model (which model to use and why)\n"
        "5. Automation Flows (visual flow descriptions: trigger → condition → action)\n"
        "6. Dashboard Spec (which metrics, which charts, which cadence)\n\n"
        "You write documentation that a technical implementer can follow exactly. "
        "Include field names, property types, and specific automation rules — not just concepts.\n\n"
        "Rules:\n"
        "- Every automation must have a clear trigger and a clear outcome\n"
        "- Every field must have a purpose — no 'nice to have' data collection\n"
        "- Design for the CRM they're actually using (HubSpot, GoHighLevel, Salesforce)\n"
        "- Include error handling: what happens when automation fails?\n"
        "- Design for scale: what happens when lead volume 10x?\n"
        "- Include data hygiene rules: deduplication, field validation, cleanup automations\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' 'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'\n\n"
        "CRM Platform Knowledge:\n"
        "- HubSpot: Free CRM, Marketing Hub, Sales Hub, Operations Hub\n"
        "- GoHighLevel: All-in-one for agencies (popular in Dubai market)\n"
        "- Salesforce: Enterprise-grade, complex but powerful\n"
        "- Pipedrive: Sales-focused, simpler pipeline management\n"
        "Default recommendation: GoHighLevel for SMBs, HubSpot for mid-market, Salesforce for enterprise."
    )

    async def design_pipeline(
        self,
        client_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Design a complete CRM pipeline architecture.

        Parameters
        ----------
        client_data : dict
            Client info including industry, sales process, team size,
            current CRM, lead sources.
        """
        task = (
            "Design a complete CRM pipeline architecture for this client.\n\n"
            "Produce:\n\n"
            "1. Pipeline Stages\n"
            "   - Stage name, definition, and entry criteria\n"
            "   - Conversion criteria to move to next stage\n"
            "   - Automation triggers at each stage transition\n"
            "   - Expected conversion rate benchmarks per stage\n"
            "   - Stage SLAs (max time in stage before alert)\n\n"
            "2. Deal Properties\n"
            "   - Required fields per stage (field name, type, options)\n"
            "   - Custom properties needed\n"
            "   - Calculated fields (deal score, probability, etc.)\n\n"
            "3. Lead Scoring Model\n"
            "   - Demographic scoring criteria (industry, size, role, location)\n"
            "   - Behavioral scoring criteria (website visits, email opens, content downloads)\n"
            "   - Score thresholds (MQL, SQL, opportunity)\n"
            "   - Score decay rules (how scores decrease over time)\n\n"
            "4. Lead Routing Rules\n"
            "   - Assignment logic (round-robin, territory, capacity-based)\n"
            "   - Escalation rules (unresponded leads, stale deals)\n"
            "   - Response time SLAs per lead source\n"
            "   - Handoff protocols between stages\n\n"
            "5. Pipeline Views & Filters\n"
            "   - Default views for sales team\n"
            "   - Manager dashboard views\n"
            "   - Alert conditions (deals stuck, SLA breach, high-value lead)\n\n"
            "Format as a technical specification document with exact field names, "
            "property types, and rule logic."
        )
        return await self.run(task=task, context=client_data, db=db, task_id=task_id)

    async def create_automation_flows(
        self,
        pipeline: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Create detailed automation flow documentation.

        Parameters
        ----------
        pipeline : dict
            Pipeline architecture (output from design_pipeline).
        """
        task = (
            "Design all automation flows for this CRM pipeline.\n\n"
            "For each flow, document:\n"
            "- Flow name and purpose\n"
            "- Trigger (what starts it)\n"
            "- Conditions (what must be true)\n"
            "- Actions (what happens, in order)\n"
            "- Error handling (what if it fails)\n"
            "- Testing checklist\n\n"
            "Required flows:\n\n"
            "1. New Lead Capture Flow\n"
            "   - Trigger: Form submission / API lead / manual entry\n"
            "   - Enrich lead data, score, assign, notify\n\n"
            "2. Lead Qualification Flow\n"
            "   - Trigger: Lead score reaches MQL threshold\n"
            "   - Create task, send internal alert, begin qualification sequence\n\n"
            "3. Stage Transition Flows (one per stage)\n"
            "   - Trigger: Deal moved to new stage\n"
            "   - Update properties, send notifications, trigger next sequence\n\n"
            "4. Stale Deal Alert Flow\n"
            "   - Trigger: Deal in stage longer than SLA\n"
            "   - Escalate, notify manager, update priority\n\n"
            "5. Won Deal Flow\n"
            "   - Trigger: Deal marked as won\n"
            "   - Create client record, trigger onboarding, update reporting\n\n"
            "6. Lost Deal Flow\n"
            "   - Trigger: Deal marked as lost\n"
            "   - Capture reason, trigger winback sequence (if appropriate), update reporting\n\n"
            "7. Data Hygiene Flow\n"
            "   - Trigger: Scheduled (daily)\n"
            "   - Deduplicate, validate fields, archive stale records\n\n"
            "Format each flow as: Trigger → [Condition] → Action 1 → Action 2 → ... → End\n"
            "Include exact field references and conditional logic."
        )
        return await self.run(
            task=task,
            context={"additional_data": f"Pipeline Architecture:\n{pipeline}"},
            db=db,
            task_id=task_id,
        )

    async def design_tracking_plan(
        self,
        client_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Design a comprehensive tracking and attribution plan.

        Parameters
        ----------
        client_data : dict
            Client info including website, tools in use,
            marketing channels, conversion goals.
        """
        task = (
            "Design a comprehensive tracking plan for this client.\n\n"
            "Produce:\n\n"
            "1. UTM Convention\n"
            "   - Source taxonomy (exact values for each traffic source)\n"
            "   - Medium taxonomy (exact values for each medium type)\n"
            "   - Campaign naming convention (format + examples)\n"
            "   - Content and term parameter usage rules\n"
            "   - UTM builder template\n\n"
            "2. Event Taxonomy\n"
            "   - Naming convention for all events (format: category_action_label)\n"
            "   - Standard events to track on every page\n"
            "   - Conversion events (micro and macro)\n"
            "   - Custom events per funnel stage\n"
            "   - Event parameters and their values\n\n"
            "3. Conversion Events\n"
            "   - Primary conversions (form submit, purchase, booking)\n"
            "   - Secondary conversions (email signup, content download, chat initiation)\n"
            "   - Event value assignment rules\n"
            "   - Cross-domain tracking requirements\n\n"
            "4. Attribution Model\n"
            "   - Recommended model (first-touch, last-touch, linear, time-decay, data-driven)\n"
            "   - Rationale for recommendation based on client's sales cycle\n"
            "   - How to configure in their analytics platform\n"
            "   - Reporting views per attribution model\n\n"
            "5. Implementation Checklist\n"
            "   - Tools to install (GA4, GTM, pixels)\n"
            "   - Tags to configure\n"
            "   - Triggers to set up\n"
            "   - Variables to define\n"
            "   - Testing procedures\n"
            "   - QA checklist\n\n"
            "Format as a technical implementation guide with exact naming conventions, "
            "code snippets where helpful, and a clear priority order."
        )
        return await self.run(task=task, context=client_data, db=db, task_id=task_id)

"""
Apex AI Marketing - Agent 6: Outbound Prospector

Model: Claude Sonnet
Engine: Outbound Engine
Language: both (EN + RU)

Writes cold outreach sequences (email + LinkedIn), researches
prospects, generates personalized angles.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class OutboundProspector(BaseAgent):
    name = "Outbound Prospector"
    role = (
        "Writes cold outreach sequences (email + LinkedIn), researches "
        "prospects, generates personalized angles."
    )
    engine = "Outbound Engine"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.8  # Slightly higher for creative outreach
    max_tokens = 4096
    language = "both"

    system_prompt = (
        "You write outreach that gets responses, not spam reports.\n\n"
        "Email rules:\n"
        "- Subject line: lowercase, casual, curiosity-driven (7 words max)\n"
        "- First line: personalized observation about THEIR business (not about us)\n"
        "- Value prop: one specific revenue leak or infrastructure problem you can identify\n"
        "- CTA: low-commitment (quick question, not 'book a call')\n"
        "- Length: 80-120 words max\n"
        "- No attachments, no HTML, no images — plain text only\n\n"
        "LinkedIn DM rules:\n"
        "- Even shorter (40-60 words)\n"
        "- Reference something specific from their profile/content\n"
        "- Ask a genuine question about their marketing infrastructure\n"
        "- NO pitch in first message\n\n"
        "Sequences:\n"
        "- Email: 4-touch over 14 days (Hook → Value → Evidence → Breakup)\n"
        "- LinkedIn: 3-touch over 10 days (Connect → Value → Soft offer)\n"
        "- Each follow-up adds new value (insight, mini-audit finding, benchmark data)\n\n"
        "For Russian-language outreach:\n"
        "- Use formal 'вы' form initially, switch to informal only if they do first\n"
        "- Reference Russian Business Council or Telegram community where relevant\n"
        "- Mention Russian-language service explicitly — it's a differentiator\n"
        "- Frame the offer as 'система' (system), not 'услуга' (service)\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' "
        "'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'"
    )

    async def research_prospect(
        self,
        company_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Research a prospect and identify personalized outreach angles.

        Parameters
        ----------
        company_data : dict
            Company name, website, industry, key person, LinkedIn URL, etc.
        """
        task = (
            "Research this prospect and identify personalized outreach angles.\n\n"
            "Produce:\n\n"
            "1. Company Overview\n"
            "   - What they do, who they serve, approximate size\n"
            "   - Their current marketing/growth infrastructure (based on what's visible)\n"
            "   - Industry position and competitive landscape\n\n"
            "2. Observable Infrastructure Gaps\n"
            "   - Website conversion path analysis (what's missing or broken)\n"
            "   - Tracking/attribution gaps (visible from outside)\n"
            "   - Content/SEO opportunities\n"
            "   - Social media and review presence assessment\n\n"
            "3. Personalization Hooks (for outreach)\n"
            "   - 3 specific observations about their business\n"
            "   - 2 relevant pain points we can address\n"
            "   - 1 genuine question to open conversation\n\n"
            "4. Recommended Outreach Strategy\n"
            "   - Which channel(s) to use (email, LinkedIn, Telegram)\n"
            "   - Which language (English, Russian, or both)\n"
            "   - Which engine(s) are most relevant to pitch\n"
            "   - Timing recommendations\n\n"
            "5. Relevance Score (1-10)\n"
            "   - How well does this prospect match our ICP?\n"
            "   - Rationale for the score\n\n"
            "Base your analysis only on publicly available information. "
            "Mark anything that requires access to verify."
        )
        return await self.run(task=task, context=company_data, db=db, task_id=task_id)

    async def generate_email_sequence(
        self,
        prospect: dict,
        language: str = "en",
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate a personalized cold email sequence.

        Parameters
        ----------
        prospect : dict
            Prospect data including company, person, pain points, angles.
        language : str
            'en' for English, 'ru' for Russian.
        """
        lang_instruction = ""
        if language == "ru":
            lang_instruction = (
                "\n\nWRITE ALL EMAILS IN RUSSIAN.\n"
                "- Use formal 'Вы' form\n"
                "- Reference Russian Business Council or Telegram community where relevant\n"
                "- Mention Russian-language service explicitly\n"
                "- Frame offers as 'система' (system), not 'услуга' (service)\n"
                "- Write natively — do NOT translate from English"
            )

        task = (
            f"Generate a 4-email cold outreach sequence for this prospect.{lang_instruction}\n\n"
            "Sequence structure:\n\n"
            "Email 1 — The Hook (Day 1)\n"
            "- Subject line: lowercase, casual, curiosity-driven (7 words max)\n"
            "- Personalized observation about their business\n"
            "- One specific revenue leak or infrastructure problem\n"
            "- Low-commitment CTA (quick question)\n"
            "- 80-120 words max, plain text\n\n"
            "Email 2 — The Value (Day 4)\n"
            "- New subject line (reply thread or fresh)\n"
            "- Share a specific insight relevant to their industry\n"
            "- Mini-audit finding or benchmark data point\n"
            "- Soft CTA (worth a conversation?)\n"
            "- 80-120 words max\n\n"
            "Email 3 — The Evidence (Day 8)\n"
            "- Reference a methodology or framework we use\n"
            "- Specific example of infrastructure problem → system solution\n"
            "- Offer a free quick infrastructure scan\n"
            "- 80-120 words max\n\n"
            "Email 4 — The Breakup (Day 14)\n"
            "- Acknowledge they're busy\n"
            "- One final value statement\n"
            "- Clear 'no hard feelings' close\n"
            "- Leave door open for future\n"
            "- 60-80 words max\n\n"
            "For each email provide:\n"
            "- Subject line\n"
            "- Body (plain text, no HTML)\n"
            "- Send timing recommendation\n"
            "- A/B variant for subject line"
        )
        context = dict(prospect)
        if language == "ru":
            context["language"] = "ru"
        return await self.run(task=task, context=context, db=db, task_id=task_id)

    async def generate_linkedin_sequence(
        self,
        prospect: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate a LinkedIn DM outreach sequence.

        Parameters
        ----------
        prospect : dict
            Prospect data including LinkedIn profile info, company, role.
        """
        task = (
            "Generate a 3-message LinkedIn DM outreach sequence for this prospect.\n\n"
            "Sequence structure:\n\n"
            "Message 1 — The Connect (Day 1, with connection request)\n"
            "- Connection request note (under 300 characters)\n"
            "- Reference something specific from their profile/content/activity\n"
            "- NO pitch — just a genuine connection reason\n\n"
            "Message 2 — The Value (Day 3-4, after they accept)\n"
            "- 40-60 words max\n"
            "- Share a specific insight relevant to their business\n"
            "- Ask a genuine question about their marketing infrastructure\n"
            "- Still no pitch\n\n"
            "Message 3 — The Soft Offer (Day 7-10)\n"
            "- 40-60 words max\n"
            "- Reference previous conversation\n"
            "- Offer something specific and low-commitment\n"
            "  (e.g., 'I mapped out 3 quick wins for businesses like yours — worth sharing?')\n"
            "- Easy yes/no response\n\n"
            "For each message provide:\n"
            "- Message text\n"
            "- Timing recommendation\n"
            "- Fallback if no response to previous message"
        )
        return await self.run(task=task, context=prospect, db=db, task_id=task_id)

    async def generate_telegram_outreach(
        self,
        topic: dict,
        language: str = "ru",
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate Telegram community outreach content.

        Parameters
        ----------
        topic : dict
            Topic data for Telegram post/outreach, target community info.
        language : str
            'en' or 'ru' (default: 'ru' for Russian community).
        """
        lang_instruction = ""
        if language == "ru":
            lang_instruction = (
                "\n\nWRITE IN RUSSIAN. Write natively — do NOT translate.\n"
                "- Professional but slightly informal tone (Telegram style)\n"
                "- Use 'Вы' form in direct messages, можно чуть свободнее в постах\n"
                "- Reference Russian business community in Dubai where relevant"
            )

        task = (
            f"Create Telegram outreach content for the Russian-speaking business community "
            f"in Dubai.{lang_instruction}\n\n"
            "Produce:\n\n"
            "1. Community Post (for posting in relevant Telegram groups)\n"
            "   - Value-first approach: share an insight, tip, or mini-analysis\n"
            "   - Subtle positioning as marketing infrastructure expert\n"
            "   - No hard sell — build authority\n"
            "   - Include a conversational CTA (DM me if...)\n"
            "   - 150-250 words\n\n"
            "2. Direct Message Templates (3 variations)\n"
            "   - For: business owner asking about marketing in the group\n"
            "   - For: someone sharing a business challenge you can help with\n"
            "   - For: cold outreach to an interesting business owner\n"
            "   - Each 40-80 words, conversational, helpful\n\n"
            "3. Follow-up Message\n"
            "   - After initial positive response\n"
            "   - Offer a free quick infrastructure scan\n"
            "   - Suggest a quick call or voice message\n\n"
            "Format as ready-to-send messages."
        )
        context = dict(topic)
        if language == "ru":
            context["language"] = "ru"
        return await self.run(task=task, context=context, db=db, task_id=task_id)

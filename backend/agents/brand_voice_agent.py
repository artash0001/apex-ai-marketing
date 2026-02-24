"""
Apex AI Marketing - Agent 13: Brand Voice Agent

Model: Claude Sonnet
Engine: All engines (consistency)
Language: both (EN + RU)

Ensures all content matches the Apex AI Marketing brand voice
AND client brand voices.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class BrandVoiceAgent(BaseAgent):
    name = "Brand Voice Agent"
    role = (
        "Ensures all content matches the Apex AI Marketing brand voice "
        "AND client brand voices."
    )
    engine = "All engines (consistency)"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.3  # Low temp for consistent evaluation
    max_tokens = 4096
    language = "both"

    system_prompt = (
        "You are the brand consistency guardian. You check every piece of content against "
        "brand guidelines.\n\n"
        "Apex AI Marketing brand voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype\n"
        "- Lead with outcomes, explain mechanisms\n"
        "- Use 'engine,' 'system,' 'infrastructure' — not 'service,' 'solution,' 'offering'\n"
        "- Never fabricate results, never use superlatives without evidence\n\n"
        "For client content, check against their brand voice guide (stored in client profile).\n\n"
        "Output: PASS (on-brand) or REVISE (with specific line-by-line feedback on what to change).\n\n"
        "Detailed Brand Voice Checklist:\n\n"
        "1. Terminology Check\n"
        "   APPROVED terms: engine, system, infrastructure, build, operate, measure, diagnose, "
        "pipeline, revenue backbone, growth infrastructure\n"
        "   BANNED terms: revolutionary, game-changing, cutting-edge, leverage, synergy, unlock, "
        "potential, innovative, disruptive, next-generation, best-in-class, world-class, "
        "turnkey, holistic, paradigm shift, thought leader\n"
        "   REPLACE: 'service' → 'engine' or 'system', 'solution' → 'system' or 'infrastructure', "
        "'offering' → 'engine' or 'engagement'\n\n"
        "2. Tone Check\n"
        "   - Is it direct and confident? (Not arrogant, not hedging)\n"
        "   - Does it lead with business outcome?\n"
        "   - Is it measurable? (Numbers > adjectives)\n"
        "   - Is it anti-hype? (Calm confidence, no exclamation marks overuse)\n\n"
        "3. Accuracy Check\n"
        "   - Are there any fabricated statistics?\n"
        "   - Are there any unverifiable claims?\n"
        "   - Are results labeled as 'verified,' 'projected,' or 'industry benchmark'?\n\n"
        "4. Language-Specific Rules\n"
        "   English:\n"
        "   - 8th-grade reading level\n"
        "   - Short sentences, short paragraphs\n"
        "   - Active voice preferred\n\n"
        "   Russian:\n"
        "   - Native writing (not translated)\n"
        "   - Formal 'Вы' in business context\n"
        "   - 'инфраструктура роста' not 'маркетинговые услуги'\n"
        "   - Delovoy (деловой) tone — direct, professional\n\n"
        "5. CTA Check\n"
        "   - Is the CTA specific? ('Request Your Infrastructure Audit' not 'Learn More')\n"
        "   - Is there exactly one primary CTA per piece?\n"
        "   - Does the CTA match the content's purpose?"
    )

    async def check_brand_voice(
        self,
        content: str,
        brand_guidelines: dict | None = None,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Check content against brand voice guidelines.

        Parameters
        ----------
        content : str
            The content to check.
        brand_guidelines : dict, optional
            Client-specific brand guidelines (if checking client content).
            If None, checks against Apex AI Marketing brand voice only.
        """
        guidelines_section = ""
        if brand_guidelines:
            guidelines_section = (
                f"\n\nClient Brand Guidelines:\n{brand_guidelines}\n\n"
                "Check against BOTH Apex brand voice AND client brand guidelines."
            )

        task = (
            f"Check this content against brand voice guidelines.{guidelines_section}\n\n"
            "Content to review:\n"
            "---\n"
            f"{content}\n"
            "---\n\n"
            "Perform a thorough brand voice audit:\n\n"
            "1. Overall Verdict: PASS or REVISE\n\n"
            "2. Terminology Audit\n"
            "   - List any banned words found (with line reference)\n"
            "   - List any terms that should be replaced\n"
            "   - Approved terminology usage score (good/needs work)\n\n"
            "3. Tone Assessment\n"
            "   - Direct and confident? (yes/no + examples)\n"
            "   - Leads with outcomes? (yes/no + examples)\n"
            "   - Measurable language? (yes/no + examples)\n"
            "   - Anti-hype? (yes/no + flag any hype language)\n\n"
            "4. Accuracy Flags\n"
            "   - Any potentially fabricated data?\n"
            "   - Any unverifiable claims?\n"
            "   - Result labeling correct?\n\n"
            "5. Line-by-Line Feedback\n"
            "   For each issue found:\n"
            "   - Quote the problematic text\n"
            "   - Explain what's wrong\n"
            "   - Provide the corrected version\n\n"
            "6. Brand Voice Score (1-10)\n"
            "   - 9-10: PASS — ready to publish\n"
            "   - 7-8: Minor revisions needed\n"
            "   - 5-6: Significant revisions needed\n"
            "   - Below 5: Rewrite recommended\n\n"
            "Be specific and constructive. Don't just flag problems — provide fixes."
        )
        return await self.run(task=task, db=db, task_id=task_id)

    async def get_revision_suggestions(
        self,
        content: str,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Get specific revision suggestions to bring content on-brand.

        Parameters
        ----------
        content : str
            The content that needs brand voice alignment.
        """
        task = (
            "This content needs to be revised to match Apex AI Marketing brand voice.\n\n"
            "Content:\n"
            "---\n"
            f"{content}\n"
            "---\n\n"
            "Provide:\n\n"
            "1. Quick Summary\n"
            "   - What's working well (keep these elements)\n"
            "   - What needs to change (overview)\n\n"
            "2. Specific Revisions (find-and-replace format)\n"
            "   For each change:\n"
            "   - FIND: [exact text to change]\n"
            "   - REPLACE WITH: [corrected text]\n"
            "   - REASON: [why this change is needed]\n\n"
            "3. Structural Suggestions\n"
            "   - Any sections that need reordering?\n"
            "   - Any sections that should be added or removed?\n"
            "   - CTA improvements?\n\n"
            "4. Revised Version\n"
            "   - Provide the COMPLETE revised content\n"
            "   - All brand voice issues fixed\n"
            "   - Ready for final review\n\n"
            "Make the minimum changes necessary to bring it on-brand. "
            "Don't rewrite everything — preserve the original intent and information."
        )
        return await self.run(task=task, db=db, task_id=task_id)

"""
Apex AI Marketing - Agent 12: Copywriter

Model: Claude Sonnet
Engine: All engines (copy support)
Language: both (EN + RU)

Writes ad copy, landing page copy, email copy, website copy —
anything persuasive.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class Copywriter(BaseAgent):
    name = "Copywriter"
    role = (
        "Writes ad copy, landing page copy, email copy, website copy — "
        "anything persuasive."
    )
    engine = "All engines (copy support)"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.8  # Higher temp for creative copy
    max_tokens = 4096
    language = "both"

    system_prompt = (
        "You write copy that converts. You use frameworks:\n"
        "- PAS (Problem-Agitate-Solution) for emails and ads\n"
        "- AIDA (Attention-Interest-Desire-Action) for landing pages\n"
        "- BAB (Before-After-Bridge) for case studies and proposals\n\n"
        "Rules:\n"
        "- Every headline must pass the 'would I click this?' test\n"
        "- Write 5 headline variations for every piece\n"
        "- Benefits over features, always\n"
        "- Short sentences. One idea per sentence.\n"
        "- Every CTA is specific ('Request Your Infrastructure Audit' not 'Learn More')\n"
        "- No cliches: 'unlock,' 'leverage,' 'synergy,' 'game-changer' are banned\n"
        "- For Russian copy: write natively with the directness Russian business readers expect\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' "
        "'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'\n\n"
        "Copy Quality Standards:\n"
        "- Every word earns its place. If removing a word doesn't change meaning, remove it.\n"
        "- Active voice over passive voice.\n"
        "- Concrete over abstract. '47% increase in leads' beats 'significant improvement.'\n"
        "- Write at 8th-grade reading level. Complex ideas, simple language.\n"
        "- Read it out loud. If it sounds stiff, rewrite.\n"
        "- The first draft is never the final draft. Always write, then cut 20%.\n\n"
        "Framework Details:\n"
        "PAS (Problem-Agitate-Solution):\n"
        "- Problem: Name the pain they feel right now\n"
        "- Agitate: Show what happens if they don't fix it (make it real)\n"
        "- Solution: Present the engine/system as the fix\n\n"
        "AIDA (Attention-Interest-Desire-Action):\n"
        "- Attention: Bold claim or surprising fact\n"
        "- Interest: 'Here's why this matters to you specifically'\n"
        "- Desire: Paint the after-state (what life looks like post-solution)\n"
        "- Action: Clear, specific, low-friction CTA\n\n"
        "BAB (Before-After-Bridge):\n"
        "- Before: Their current painful state\n"
        "- After: The desired outcome state\n"
        "- Bridge: How the engine/system gets them there"
    )

    async def write_ad_copy(
        self,
        brief: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Write ad copy for multiple platforms.

        Parameters
        ----------
        brief : dict
            Product/service info, target audience, platform(s),
            character limits, USPs.
        """
        task = (
            "Write ad copy based on this brief.\n\n"
            "Produce:\n\n"
            "1. Headlines (5 variations)\n"
            "   - Each passes the 'would I click this?' test\n"
            "   - Mix of: benefit-driven, curiosity-driven, proof-driven\n"
            "   - Include character count for each\n\n"
            "2. Primary Ad Copy (3 variations using PAS framework)\n"
            "   Variation 1: Problem-focused\n"
            "   Variation 2: Outcome-focused\n"
            "   Variation 3: Social proof-focused\n\n"
            "3. CTA Options (3 variations)\n"
            "   - Specific, action-oriented\n"
            "   - Not generic ('Learn More' is banned)\n\n"
            "4. Platform-Specific Adaptations\n"
            "   - If Google Ads: respect 30-char headline, 90-char description limits\n"
            "   - If Meta: hook in first 125 chars\n"
            "   - If LinkedIn: professional B2B tone\n\n"
            "5. A/B Test Recommendations\n"
            "   - Which elements to test first\n"
            "   - Control vs. variant suggestions\n\n"
            "Each piece of copy should be ready to deploy. "
            "Include character counts where limits apply."
        )
        return await self.run(task=task, context=brief, db=db, task_id=task_id)

    async def write_landing_page(
        self,
        brief: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Write landing page copy using AIDA framework.

        Parameters
        ----------
        brief : dict
            Offer, target audience, traffic source, awareness level, proof elements.
        """
        task = (
            "Write complete landing page copy using the AIDA framework.\n\n"
            "Produce:\n\n"
            "1. Above the Fold\n"
            "   - Headline (5 variations — outcome-focused)\n"
            "   - Subheadline (mechanism — how it works)\n"
            "   - CTA button text (3 variations — specific)\n"
            "   - Proof element (what to display: number, testimonial, logos)\n\n"
            "2. Problem Section\n"
            "   - 3-4 pain points in customer language\n"
            "   - 'Sound familiar?' or equivalent bridge\n\n"
            "3. Solution Section\n"
            "   - How the engine/system solves their problem\n"
            "   - 3 key benefits (with supporting details)\n"
            "   - Process overview (3-4 simple steps)\n\n"
            "4. Proof Section\n"
            "   - Testimonial placement guidance (do NOT fabricate)\n"
            "   - Results format (numbers, before/after)\n"
            "   - Trust elements (badges, certifications, client logos)\n\n"
            "5. Objection Handling (FAQ)\n"
            "   - Top 5 objections answered\n"
            "   - Each answer is concise and builds confidence\n\n"
            "6. Final CTA Section\n"
            "   - Urgency element (if appropriate)\n"
            "   - Risk reversal (guarantee, free audit, etc.)\n"
            "   - CTA button + supporting microcopy\n\n"
            "All copy should be scannable, mobile-friendly (short paragraphs), "
            "and ready for a designer to implement."
        )
        return await self.run(task=task, context=brief, db=db, task_id=task_id)

    async def write_email_copy(
        self,
        brief: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Write email copy using PAS framework.

        Parameters
        ----------
        brief : dict
            Email type, audience, goal, context, offers.
        """
        task = (
            "Write email copy based on this brief.\n\n"
            "Produce:\n\n"
            "1. Subject Lines (5 variations)\n"
            "   - 6-10 words each\n"
            "   - Mix: benefit, curiosity, urgency, personalized\n"
            "   - Include preview text for each\n\n"
            "2. Email Body (using PAS framework)\n"
            "   - Problem: Name the pain (1-2 sentences)\n"
            "   - Agitate: What happens if unresolved (1-2 sentences)\n"
            "   - Solution: How the engine/system fixes it (2-3 sentences)\n"
            "   - CTA: Specific next step (1 sentence)\n\n"
            "3. Alternative Version (using BAB framework)\n"
            "   - Before: Current state\n"
            "   - After: Desired state\n"
            "   - Bridge: How to get there\n\n"
            "4. Format Notes\n"
            "   - Mobile-first: short paragraphs\n"
            "   - One idea per paragraph\n"
            "   - One CTA (not multiple competing actions)\n"
            "   - Plain text version (no HTML dependencies)\n\n"
            "If Russian version requested, write natively, not translated."
        )
        return await self.run(task=task, context=brief, db=db, task_id=task_id)

    async def write_headlines(
        self,
        topic: dict,
        count: int = 5,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Write multiple headline variations for a topic.

        Parameters
        ----------
        topic : dict
            The topic, angle, audience, platform, and any constraints.
        count : int
            Number of headlines to write (default: 5).
        """
        task = (
            f"Write {count} headline variations for this topic.\n\n"
            "For each headline provide:\n"
            "1. The headline text\n"
            "2. Character count\n"
            "3. Framework used (benefit, curiosity, proof, urgency, question)\n"
            "4. Best platform/use case for this headline\n"
            "5. Why it works (1 sentence)\n\n"
            "Rules:\n"
            "- Every headline must pass the 'would I click this?' test\n"
            "- Benefits over features\n"
            "- Specific over vague ('47% more leads' beats 'more leads')\n"
            "- No banned words: 'revolutionary,' 'game-changing,' 'unlock,' 'leverage'\n"
            "- Include at least one question-format headline\n"
            "- Include at least one number-driven headline\n\n"
            "If Russian version requested, write native Russian headlines — "
            "not translations of English ones."
        )
        context = dict(topic)
        context["additional_data"] = f"Count: {count}"
        return await self.run(task=task, context=context, db=db, task_id=task_id)

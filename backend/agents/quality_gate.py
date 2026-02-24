"""
Apex AI Marketing - Agent 14: Quality Gate

Model: Claude Opus (needs judgment)
Engine: All engines (final review)
Language: both (EN + RU)

Reviews ALL content before it goes to clients.
Nothing ships without Quality Gate approval.
"""

from agents.base_agent import BaseAgent, AgentOutput, ReviewResult
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class QualityGate(BaseAgent):
    name = "Quality Gate"
    role = (
        "Reviews ALL content before it goes to clients. "
        "Nothing ships without Quality Gate approval."
    )
    engine = "All engines (final review)"
    model = settings.PREMIUM_MODEL  # Claude Opus
    temperature = 0.3  # Low temp for consistent judgment
    max_tokens = 6144
    language = "both"

    system_prompt = (
        "You are the final quality gate. Nothing goes to a client without your approval.\n\n"
        "Review checklist:\n"
        "1. Brand voice consistency (matches Apex voice AND client brand guide)\n"
        "2. Factual accuracy (NO fabricated statistics, NO hallucinated claims, NO made-up data)\n"
        "3. Grammar and clarity (Hemingway score ≤ Grade 10)\n"
        "4. Strategic alignment (does this serve the engine's goal?)\n"
        "5. Deliverable completeness (all promised items included?)\n"
        "6. Scope compliance (nothing outside the defined engine scope?)\n"
        "7. CTA present and clear\n"
        "8. No banned words ('revolutionary,' 'game-changing,' 'leverage,' 'synergy,' 'unlock')\n"
        "9. Proof claims verified (any result cited must be labeled as 'verified,' 'projected,' "
        "or 'industry benchmark')\n\n"
        "Output:\n"
        "- APPROVED: Ready for client delivery\n"
        "- REVISE: Specific feedback for the producing agent (line-level corrections)\n"
        "- REJECT: Fundamental issue, needs complete redo (rare — explain why)\n\n"
        "You are constructive but strict. Mediocre deliverables damage the agency's "
        "positioning as 'infrastructure,' not 'services.'\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' "
        "'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'\n\n"
        "Review Standards by Deliverable Type:\n\n"
        "Audit Reports:\n"
        "- All 6 sections present and substantive\n"
        "- No fabricated data (all claims sourced or marked 'requires access')\n"
        "- Recommendations tied to specific engines\n"
        "- Actionable, with timelines and priorities\n\n"
        "Content (articles, briefs):\n"
        "- 8th-grade reading level\n"
        "- No filler content\n"
        "- Clear CTA tied to engine\n"
        "- SEO specs complete (meta title, description, schema)\n\n"
        "Outreach (emails, LinkedIn, Telegram):\n"
        "- Within character/word limits\n"
        "- Personalized (not generic)\n"
        "- No spam triggers\n"
        "- Low-commitment CTA\n\n"
        "Proposals/SOWs:\n"
        "- All 10 sections present\n"
        "- Pricing accurate\n"
        "- Scope clearly defined (inclusions AND exclusions)\n"
        "- No false promises\n\n"
        "Reports:\n"
        "- No fabricated metrics\n"
        "- Insights, not just data dumps\n"
        "- Action items with owners and deadlines\n"
        "- Comparison to targets and previous period"
    )

    async def review_deliverable(
        self,
        content: str,
        deliverable_type: str,
        client_data: dict | None = None,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Review a deliverable against the 9-point quality checklist.

        Parameters
        ----------
        content : str
            The content to review.
        deliverable_type : str
            Type: 'audit', 'article', 'email', 'proposal', 'report',
            'ad_copy', 'landing_page', 'sequence', 'dashboard_spec'.
        client_data : dict, optional
            Client profile for context (brand guide, engine scope, etc.).
        """
        client_context = ""
        if client_data:
            client_context = f"\n\nClient Context:\n{client_data}\n"

        task = (
            f"Review this {deliverable_type} deliverable against the 9-point quality checklist."
            f"{client_context}\n\n"
            "Content to review:\n"
            "---\n"
            f"{content}\n"
            "---\n\n"
            "Evaluate against EACH of the 9 criteria:\n\n"
            "1. Brand Voice Consistency\n"
            "   - PASS / FAIL\n"
            "   - Specific issues found (if any)\n\n"
            "2. Factual Accuracy\n"
            "   - PASS / FAIL\n"
            "   - Any fabricated or unverifiable claims?\n"
            "   - Are cited results properly labeled?\n\n"
            "3. Grammar and Clarity\n"
            "   - PASS / FAIL\n"
            "   - Reading level assessment\n"
            "   - Grammar issues found\n\n"
            "4. Strategic Alignment\n"
            "   - PASS / FAIL\n"
            "   - Does it serve the engine's goal?\n"
            "   - Is it appropriate for the client's stage?\n\n"
            "5. Deliverable Completeness\n"
            "   - PASS / FAIL\n"
            "   - Missing sections or elements?\n"
            "   - Are all promised items included?\n\n"
            "6. Scope Compliance\n"
            "   - PASS / FAIL\n"
            "   - Anything outside the defined scope?\n"
            "   - Anything that could create scope creep expectations?\n\n"
            "7. CTA Present and Clear\n"
            "   - PASS / FAIL\n"
            "   - Is the CTA specific and actionable?\n"
            "   - Is there exactly one primary CTA?\n\n"
            "8. No Banned Words\n"
            "   - PASS / FAIL\n"
            "   - List any banned words found\n\n"
            "9. Proof Claims Verified\n"
            "   - PASS / FAIL\n"
            "   - Are all results labeled as verified/projected/benchmark?\n"
            "   - Any claims that need source attribution?\n\n"
            "Final Verdict:\n"
            "- APPROVED: All 9 criteria pass (or minor issues noted but acceptable)\n"
            "- REVISE: 1-3 criteria fail (provide specific line-level corrections)\n"
            "- REJECT: 4+ criteria fail or fundamental quality issue\n\n"
            "Quality Score: [0-10]\n\n"
            "For REVISE verdicts, provide specific, actionable feedback the producing "
            "agent can use to fix the issues. Include exact text to change and "
            "suggested replacements."
        )
        return await self.run(task=task, db=db, task_id=task_id)

    async def full_review_pipeline(
        self,
        content: str,
        producing_agent: str,
        deliverable_type: str = "general",
        client_data: dict | None = None,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Run the full review pipeline: quality check + brand voice + recommendations.

        Parameters
        ----------
        content : str
            The content to review.
        producing_agent : str
            Name of the agent that produced this content.
        deliverable_type : str
            Type of deliverable.
        client_data : dict, optional
            Client profile for context.
        """
        client_context = ""
        if client_data:
            client_context = f"\nClient Context:\n{client_data}\n"

        task = (
            f"Full review pipeline for content produced by {producing_agent}.\n"
            f"Deliverable type: {deliverable_type}\n"
            f"{client_context}\n"
            "Content:\n"
            "---\n"
            f"{content}\n"
            "---\n\n"
            "Run the complete review pipeline:\n\n"
            "STEP 1: Quality Checklist (9 criteria)\n"
            "   Review each of the 9 criteria as described in your checklist.\n"
            "   Score each: PASS or FAIL with notes.\n\n"
            "STEP 2: Brand Voice Deep Check\n"
            "   - Terminology audit (banned words, preferred terms)\n"
            "   - Tone assessment (direct, confident, anti-hype)\n"
            "   - Accuracy check (no fabrications)\n\n"
            "STEP 3: Deliverable-Type-Specific Check\n"
            f"   Apply the specific standards for '{deliverable_type}' deliverables.\n\n"
            "STEP 4: Improvement Recommendations\n"
            "   - Top 3 things that would improve this deliverable\n"
            "   - Specific text changes (find → replace format)\n"
            "   - Structural suggestions (if any)\n\n"
            "STEP 5: Final Verdict\n"
            "   - APPROVED / REVISE / REJECT\n"
            "   - Overall quality score (0-10)\n"
            "   - Summary feedback for {producing_agent}\n"
            "   - If REVISE: specific revision instructions\n"
            "   - If REJECT: explanation and recommendation\n\n"
            "Be thorough but constructive. The goal is to make every deliverable "
            "excellent, not to find fault."
        )
        return await self.run(task=task, db=db, task_id=task_id)

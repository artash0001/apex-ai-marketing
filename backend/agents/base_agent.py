"""
Apex AI Marketing - Base Agent

Abstract base class for all 15 AI agents. Handles Claude API interaction,
cost tracking, structured output, and review/iteration loops.
"""

import logging
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from services.ai_service import AIService, AIResponse

logger = logging.getLogger(__name__)
settings = get_settings()


# ── Pydantic output models ────────────────────────────────────────────

class AgentOutput(BaseModel):
    """Structured output from an agent run."""

    content: str = Field(..., description="The generated content / deliverable text")
    agent_name: str = Field(..., description="Name of the agent that produced this")
    model: str = Field(..., description="Claude model used")
    input_tokens: int = Field(0, description="Input tokens consumed")
    output_tokens: int = Field(0, description="Output tokens consumed")
    cost: Decimal = Field(Decimal("0"), description="Cost of this run in USD")
    metadata: dict = Field(default_factory=dict, description="Extra metadata")


class ReviewResult(BaseModel):
    """Result of a content review."""

    verdict: str = Field(
        ...,
        description="APPROVED | REVISE | REJECT",
    )
    score: float = Field(
        0.0,
        description="Quality score 0-10",
    )
    feedback: str = Field(
        "",
        description="Detailed line-level feedback",
    )
    criteria_results: dict = Field(
        default_factory=dict,
        description="Per-criterion pass/fail with notes",
    )


# ── Base Agent ────────────────────────────────────────────────────────

class BaseAgent:
    """Base class for all Apex AI Marketing agents.

    Subclasses should set class-level attributes and optionally override
    ``build_system_prompt`` for dynamic prompt construction.

    Example subclass::

        class InfrastructureAuditor(BaseAgent):
            name = "Infrastructure Auditor"
            role = "Diagnoses funnels, tracking gaps, and revenue leaks."
            engine = "Growth Infrastructure Audit"
            model = settings.PREMIUM_MODEL
            temperature = 0.4
            max_tokens = 8192
            language = "both"
            system_prompt = "You are the Infrastructure Auditor at Apex AI Marketing..."
    """

    # ── Override these in subclasses ──────────────────────────────────
    name: str = "BaseAgent"
    role: str = ""
    engine: str = ""
    system_prompt: str = ""
    model: str = settings.DEFAULT_MODEL
    temperature: float = 0.7
    max_tokens: int = 4096
    language: str = "en"  # "en", "ru", or "both"

    def __init__(self, ai_service: AIService | None = None) -> None:
        self._ai = ai_service or AIService()

    # ── Build system prompt (override for dynamic prompts) ────────────
    def build_system_prompt(self, context: dict | None = None) -> str:
        """Return the system prompt, optionally enriched with context.

        Override in subclasses to inject client brand voice, language
        preferences, or other dynamic data.
        """
        base = self.system_prompt
        if context and context.get("language") == "ru":
            base += (
                "\n\nIMPORTANT: Respond in Russian. Write natively — "
                "do NOT translate from English."
            )
        if context and context.get("brand_voice"):
            base += (
                f"\n\nClient brand voice guidelines:\n{context['brand_voice']}"
            )
        return base

    # ── Main run method ───────────────────────────────────────────────
    async def run(
        self,
        task: str,
        context: dict | None = None,
        db: AsyncSession | None = None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Execute the agent on a task.

        Parameters
        ----------
        task : str
            The task description / user message.
        context : dict, optional
            Additional context (client info, brand voice, etc.).
        db : AsyncSession, optional
            Database session for cost tracking.
        task_id : str, optional
            Link the usage to a specific Task record.

        Returns
        -------
        AgentOutput
            Structured output with content, cost, and metadata.
        """
        ctx = context or {}
        system = self.build_system_prompt(ctx)

        # Enrich the user message with context if available
        user_message = task
        if ctx.get("client_name"):
            user_message = f"Client: {ctx['client_name']}\n\n{task}"
        if ctx.get("additional_data"):
            user_message += f"\n\nAdditional data:\n{ctx['additional_data']}"

        response: AIResponse = await self._ai.generate(
            agent_name=self.name,
            system_prompt=system,
            user_message=user_message,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            db=db,
            task_id=task_id,
        )

        return AgentOutput(
            content=response.content,
            agent_name=self.name,
            model=response.model,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            cost=response.cost,
            metadata={
                "engine": self.engine,
                "language": self.language,
                "stop_reason": response.stop_reason,
            },
        )

    # ── Review method ─────────────────────────────────────────────────
    async def review(
        self,
        content: str,
        criteria: list[str] | None = None,
        db: AsyncSession | None = None,
    ) -> ReviewResult:
        """Review a piece of content against specified criteria.

        Parameters
        ----------
        content : str
            The content to review.
        criteria : list[str], optional
            Specific criteria to evaluate against.
        db : AsyncSession, optional
            Database session for cost tracking.

        Returns
        -------
        ReviewResult
            Verdict (APPROVED / REVISE / REJECT) with detailed feedback.
        """
        criteria = criteria or [
            "Brand voice consistency",
            "Factual accuracy (no fabricated data)",
            "Grammar and clarity",
            "Strategic alignment",
            "Completeness",
            "No banned words",
        ]

        criteria_text = "\n".join(f"- {c}" for c in criteria)

        review_prompt = f"""Review the following content against these criteria:

{criteria_text}

Content to review:
---
{content}
---

Respond in this exact format:
VERDICT: [APPROVED or REVISE or REJECT]
SCORE: [0-10]
FEEDBACK: [Detailed line-level feedback]
CRITERIA_RESULTS:
{chr(10).join(f'- {c}: [PASS or FAIL] - [notes]' for c in criteria)}"""

        response = await self._ai.generate(
            agent_name=f"{self.name} (Review)",
            system_prompt="You are a strict quality reviewer. Be constructive but thorough.",
            user_message=review_prompt,
            model=self.model,
            temperature=0.3,
            max_tokens=2048,
            db=db,
        )

        # Parse the structured response
        text = response.content
        verdict = "REVISE"
        score = 5.0
        feedback = text

        for line in text.split("\n"):
            line_stripped = line.strip()
            if line_stripped.startswith("VERDICT:"):
                v = line_stripped.replace("VERDICT:", "").strip().upper()
                if v in ("APPROVED", "REVISE", "REJECT"):
                    verdict = v
            elif line_stripped.startswith("SCORE:"):
                try:
                    score = float(line_stripped.replace("SCORE:", "").strip())
                except ValueError:
                    pass

        return ReviewResult(
            verdict=verdict,
            score=score,
            feedback=feedback,
            criteria_results={c: "see feedback" for c in criteria},
        )

    # ── Iterate method ────────────────────────────────────────────────
    async def iterate(
        self,
        content: str,
        feedback: str,
        db: AsyncSession | None = None,
    ) -> str:
        """Revise content based on review feedback.

        Parameters
        ----------
        content : str
            The original content that needs revision.
        feedback : str
            The reviewer's feedback explaining what to change.
        db : AsyncSession, optional
            Database session for cost tracking.

        Returns
        -------
        str
            The revised content.
        """
        iteration_prompt = f"""You previously produced this content:

---
{content}
---

The reviewer provided this feedback:

---
{feedback}
---

Please revise the content to address ALL feedback points. Return ONLY the revised content, no explanations."""

        response = await self._ai.generate(
            agent_name=f"{self.name} (Iteration)",
            system_prompt=self.build_system_prompt(),
            user_message=iteration_prompt,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            db=db,
        )

        return response.content

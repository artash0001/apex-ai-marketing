"""
Apex AI Marketing - AI Service

Wraps the Anthropic Claude API with cost tracking, retries, and
support for multiple models (Sonnet for speed, Opus for strategy).
"""

import logging
from decimal import Decimal
from dataclasses import dataclass

import anthropic
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from models.ai_usage import AIUsage

logger = logging.getLogger(__name__)
settings = get_settings()

# ── Cost per 1M tokens (USD) ─────────────────────────────────────────
# Update these when Anthropic changes pricing.
MODEL_PRICING: dict[str, dict[str, float]] = {
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
    "claude-opus-4-20250514": {"input": 15.00, "output": 75.00},
}

DEFAULT_PRICING = {"input": 3.00, "output": 15.00}


@dataclass
class AIResponse:
    """Structured response from the Claude API."""

    content: str
    model: str
    input_tokens: int
    output_tokens: int
    cost: Decimal
    stop_reason: str | None = None


class AIService:
    """Claude API wrapper with cost tracking and retry logic.

    Usage::

        svc = AIService()
        response = await svc.generate(
            agent_name="Infrastructure Auditor",
            system_prompt="You are ...",
            user_message="Audit this website: ...",
        )
        print(response.content, response.cost)
    """

    def __init__(self) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    # ── Main generation method ────────────────────────────────────────
    async def generate(
        self,
        agent_name: str,
        system_prompt: str,
        user_message: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        db: AsyncSession | None = None,
        task_id: str | None = None,
    ) -> AIResponse:
        """Send a prompt to Claude and return the response with cost data.

        Parameters
        ----------
        agent_name : str
            Name of the calling agent (for cost attribution).
        system_prompt : str
            System-level instructions for the model.
        user_message : str
            The user-facing prompt.
        model : str, optional
            Model identifier. Defaults to ``settings.DEFAULT_MODEL``.
        temperature : float
            Sampling temperature (0.0 - 1.0).
        max_tokens : int
            Maximum tokens in the response.
        db : AsyncSession, optional
            If provided, the usage record is persisted to the ai_usage table.
        task_id : str, optional
            Link the usage record to a specific task.
        """
        model = model or settings.DEFAULT_MODEL
        max_retries = 3

        last_error: Exception | None = None
        for attempt in range(1, max_retries + 1):
            try:
                message = await self._client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_message}],
                )
                break
            except anthropic.RateLimitError as exc:
                last_error = exc
                logger.warning(
                    "Rate limited (attempt %d/%d) for agent=%s",
                    attempt,
                    max_retries,
                    agent_name,
                )
                if attempt == max_retries:
                    raise
                import asyncio
                await asyncio.sleep(2 ** attempt)
            except anthropic.APIStatusError as exc:
                last_error = exc
                logger.error(
                    "API error (attempt %d/%d) for agent=%s: %s",
                    attempt,
                    max_retries,
                    agent_name,
                    exc,
                )
                if attempt == max_retries:
                    raise
                import asyncio
                await asyncio.sleep(2 ** attempt)
        else:
            raise last_error  # type: ignore[misc]

        # ── Extract response ──────────────────────────────────────────
        content = message.content[0].text if message.content else ""
        input_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens
        stop_reason = message.stop_reason

        # ── Calculate cost ────────────────────────────────────────────
        pricing = MODEL_PRICING.get(model, DEFAULT_PRICING)
        cost = Decimal(str(
            (input_tokens * pricing["input"] / 1_000_000)
            + (output_tokens * pricing["output"] / 1_000_000)
        ))

        logger.info(
            "AI call: agent=%s model=%s in=%d out=%d cost=$%s",
            agent_name,
            model,
            input_tokens,
            output_tokens,
            cost,
        )

        # ── Persist usage record ──────────────────────────────────────
        if db is not None:
            usage = AIUsage(
                agent_name=agent_name,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                task_id=task_id,
            )
            db.add(usage)
            await db.flush()

        return AIResponse(
            content=content,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            stop_reason=stop_reason,
        )

    # ── Convenience: generate with Opus ───────────────────────────────
    async def generate_premium(
        self,
        agent_name: str,
        system_prompt: str,
        user_message: str,
        **kwargs,
    ) -> AIResponse:
        """Same as ``generate`` but forces the premium (Opus) model."""
        return await self.generate(
            agent_name=agent_name,
            system_prompt=system_prompt,
            user_message=user_message,
            model=settings.PREMIUM_MODEL,
            **kwargs,
        )

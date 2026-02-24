"""
Apex AI Marketing - Agent 10: Experiment Runner

Model: Claude Sonnet
Engine: Growth Ops Retainer
Language: en

Designs, documents, and evaluates A/B tests and marketing experiments.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class ExperimentRunner(BaseAgent):
    name = "Experiment Runner"
    role = "Designs, documents, and evaluates A/B tests and marketing experiments."
    engine = "Growth Ops Retainer"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.4  # Low temp for analytical precision
    max_tokens = 4096
    language = "en"

    system_prompt = (
        "You run structured marketing experiments. Every test has a hypothesis, a method, "
        "a success metric, and a learning.\n\n"
        "Experiment log format:\n"
        "1. Experiment ID + Date\n"
        "2. Hypothesis ('We believe [change] will [effect] because [reason]')\n"
        "3. What we changed (specific variable)\n"
        "4. What we measured (primary metric + guardrail metrics)\n"
        "5. Duration + sample size\n"
        "6. Result (data)\n"
        "7. Decision (implement / iterate / discard)\n"
        "8. Learning (what we now know that we didn't before)\n\n"
        "Rules:\n"
        "- Test ONE variable at a time\n"
        "- Define success criteria BEFORE running the test\n"
        "- Minimum 7-day run for any experiment (avoid day-of-week bias)\n"
        "- Document EVERY experiment, including failures — they build credibility\n"
        "- Recommend next experiment based on learnings\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' "
        "'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'\n\n"
        "Statistical Rigor:\n"
        "- Always specify confidence level required (typically 95%)\n"
        "- Calculate minimum sample size before starting\n"
        "- Use appropriate statistical test (chi-square for conversion, t-test for continuous)\n"
        "- Report p-values and confidence intervals when data is available\n"
        "- Account for multiple comparisons when running parallel tests\n"
        "- Flag any validity threats (sample contamination, external events, etc.)"
    )

    async def design_experiment(
        self,
        hypothesis_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Design a structured marketing experiment.

        Parameters
        ----------
        hypothesis_data : dict
            The hypothesis, channel/engine, current performance, goals.
        """
        task = (
            "Design a structured marketing experiment based on this hypothesis.\n\n"
            "Produce the complete experiment plan:\n\n"
            "1. Experiment Overview\n"
            "   - Experiment ID (format: EXP-[YYYY]-[NNN])\n"
            "   - Engine / channel this applies to\n"
            "   - Priority level (high, medium, low)\n\n"
            "2. Hypothesis\n"
            "   - Statement: 'We believe [change] will [effect] because [reason]'\n"
            "   - Null hypothesis: What we expect if the change has no effect\n\n"
            "3. Experiment Design\n"
            "   - Variable to test (ONE variable only)\n"
            "   - Control: What stays the same\n"
            "   - Variant: What changes (be specific)\n"
            "   - Target audience / segment\n"
            "   - Traffic split (typically 50/50)\n\n"
            "4. Metrics\n"
            "   - Primary metric (the ONE thing we're measuring)\n"
            "   - Secondary metrics (supporting data)\n"
            "   - Guardrail metrics (what we don't want to hurt)\n"
            "   - Success criteria (specific threshold, e.g., '15% improvement')\n\n"
            "5. Logistics\n"
            "   - Minimum sample size calculation\n"
            "   - Estimated duration (minimum 7 days)\n"
            "   - Tools needed for implementation and measurement\n"
            "   - Implementation steps (who does what)\n\n"
            "6. Analysis Plan\n"
            "   - Statistical test to use\n"
            "   - Confidence level required\n"
            "   - When to check results (avoid peeking bias)\n"
            "   - Decision framework: implement if X, iterate if Y, discard if Z\n\n"
            "7. Risk Assessment\n"
            "   - What could invalidate results\n"
            "   - Mitigation strategies\n"
            "   - Rollback plan if variant performs significantly worse\n\n"
            "Format as a complete experiment brief that a team can execute."
        )
        return await self.run(task=task, context=hypothesis_data, db=db, task_id=task_id)

    async def evaluate_experiment(
        self,
        experiment_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Evaluate a completed experiment and document the results.

        Parameters
        ----------
        experiment_data : dict
            The experiment plan, raw results data, sample sizes, duration.
        """
        task = (
            "Evaluate this completed experiment and document the results.\n\n"
            "Produce:\n\n"
            "1. Experiment Summary\n"
            "   - Experiment ID and dates run\n"
            "   - Hypothesis reminder\n"
            "   - Duration and sample size achieved\n\n"
            "2. Results\n"
            "   - Primary metric: Control vs. Variant\n"
            "   - Absolute difference and relative change (%)\n"
            "   - Statistical significance (p-value, confidence interval)\n"
            "   - Secondary metrics comparison\n"
            "   - Guardrail metrics status (any negative impacts?)\n\n"
            "3. Data Quality Assessment\n"
            "   - Was sample size sufficient?\n"
            "   - Any external factors that may have influenced results?\n"
            "   - Data collection issues?\n"
            "   - Confidence level in the results\n\n"
            "4. Decision\n"
            "   - IMPLEMENT: Result is significant and positive → roll out to 100%\n"
            "   - ITERATE: Promising but not conclusive → modify and re-test\n"
            "   - DISCARD: No improvement or negative impact → revert\n"
            "   - Specific rationale for the decision\n\n"
            "5. Learning\n"
            "   - What we now know that we didn't before\n"
            "   - How this changes our understanding of the channel/audience\n"
            "   - Implications for future experiments\n\n"
            "6. Next Steps\n"
            "   - If IMPLEMENT: rollout plan and timeline\n"
            "   - If ITERATE: what to change in the next version\n"
            "   - If DISCARD: alternative hypothesis to test\n"
            "   - Recommended next experiment based on learnings\n\n"
            "Be honest about ambiguous results. 'We don't have enough data to conclude' "
            "is a valid finding."
        )
        return await self.run(
            task=task,
            context={"additional_data": f"Experiment Data:\n{experiment_data}"},
            db=db,
            task_id=task_id,
        )

    async def recommend_next_experiment(
        self,
        learnings: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Recommend the next experiment based on accumulated learnings.

        Parameters
        ----------
        learnings : dict
            Previous experiment results, current performance data,
            active engines, and strategic goals.
        """
        task = (
            "Based on accumulated experiment learnings and current performance data, "
            "recommend the next 3-5 experiments to run.\n\n"
            "For each recommended experiment:\n\n"
            "1. Experiment Name\n"
            "2. Hypothesis (full format: 'We believe... will... because...')\n"
            "3. Rationale\n"
            "   - Why this experiment now? (based on learnings)\n"
            "   - Expected revenue impact if hypothesis is correct\n"
            "   - Confidence level in hypothesis (low/medium/high)\n\n"
            "4. Difficulty\n"
            "   - Implementation effort (low/medium/high)\n"
            "   - Time to result\n"
            "   - Resources needed\n\n"
            "5. Priority Score\n"
            "   - Score based on: expected impact × confidence ÷ effort\n"
            "   - Rank all recommendations by this score\n\n"
            "Also include:\n"
            "- Experiment calendar (what to run when)\n"
            "- Dependencies between experiments\n"
            "- How experiments connect to engine KPIs\n"
            "- Budget impact estimate\n\n"
            "Prioritize experiments that:\n"
            "1. Address the biggest performance gap\n"
            "2. Build on learnings from previous experiments\n"
            "3. Can be implemented quickly\n"
            "4. Have the highest expected revenue impact"
        )
        return await self.run(
            task=task,
            context={"additional_data": f"Learnings & Context:\n{learnings}"},
            db=db,
            task_id=task_id,
        )

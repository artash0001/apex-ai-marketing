"""
Apex AI Marketing - Agent 7: Ad Systems Agent

Model: Claude Sonnet
Engine: Paid Acquisition Engine
Language: en

Creates ad copy, landing page copy, campaign structure
recommendations, and A/B test plans.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class AdSystemsAgent(BaseAgent):
    name = "Ad Systems Agent"
    role = (
        "Creates ad copy, landing page copy, campaign structure "
        "recommendations, and A/B test plans."
    )
    engine = "Paid Acquisition Engine"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.7
    max_tokens = 6144
    language = "en"

    system_prompt = (
        "You write ads that convert within strict character limits and create landing pages "
        "that close.\n\n"
        "Google Ads: 15 headlines (30 chars) + 4 descriptions (90 chars) for responsive search ads.\n"
        "Meta Ads: 3 complete variants — hook in first 125 chars, headline 40 chars, "
        "description 30 chars.\n"
        "LinkedIn Ads: Professional tone, B2B-focused, problem-aware messaging.\n\n"
        "Landing pages:\n"
        "- One page, one offer, one CTA\n"
        "- Above-the-fold: headline (outcome), subhead (mechanism), CTA, proof element\n"
        "- Below-fold: problem → solution → social proof → objection handling → final CTA\n"
        "- Every element earns its place — no filler sections\n\n"
        "Rules:\n"
        "- Numbers beat words ('Save 47%' not 'Save almost half')\n"
        "- Address objections in the ad copy itself\n"
        "- Write for the buyer's awareness level (cold/warm/hot)\n"
        "- Every ad connects to a specific landing page — no generic homepages\n"
        "- Track everything: UTMs on every link, conversion events on every CTA\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' "
        "'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'"
    )

    async def generate_google_ads(
        self,
        product_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate Google Ads responsive search ad components.

        Parameters
        ----------
        product_data : dict
            Product/service info, target keywords, USPs, audience.
        """
        task = (
            "Create a complete Google Ads responsive search ad set.\n\n"
            "Produce:\n\n"
            "1. Campaign Structure\n"
            "   - Campaign name and objective\n"
            "   - Ad group structure (themes/keyword groups)\n"
            "   - Target keywords per ad group (10-20 each)\n"
            "   - Negative keyword list\n"
            "   - Match type recommendations\n\n"
            "2. Responsive Search Ad Components (per ad group)\n"
            "   - 15 Headlines (max 30 characters each)\n"
            "     * Pin-worthy headlines for positions 1, 2, 3\n"
            "     * Keyword-inclusive headlines\n"
            "     * Benefit-driven headlines\n"
            "     * CTA headlines\n"
            "     * Social proof headlines\n"
            "   - 4 Descriptions (max 90 characters each)\n"
            "     * Problem-aware description\n"
            "     * Benefit-focused description\n"
            "     * CTA-driven description\n"
            "     * Proof/credibility description\n\n"
            "3. Sitelink Extensions (4)\n"
            "   - Sitelink title (25 chars) + description (35 chars x2) + URL path\n\n"
            "4. Callout Extensions (6)\n"
            "   - Max 25 characters each\n\n"
            "5. Structured Snippets\n"
            "   - Header type + values\n\n"
            "6. UTM Parameters\n"
            "   - UTM template for each ad group\n\n"
            "7. Landing Page URL Recommendations\n"
            "   - Which landing page for each ad group\n"
            "   - URL path structure\n\n"
            "Ensure all headlines and descriptions respect character limits exactly."
        )
        return await self.run(task=task, context=product_data, db=db, task_id=task_id)

    async def generate_meta_ads(
        self,
        product_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate Meta (Facebook/Instagram) ad variants.

        Parameters
        ----------
        product_data : dict
            Product/service info, target audience, creative direction.
        """
        task = (
            "Create 3 complete Meta (Facebook + Instagram) ad variants.\n\n"
            "For each variant, produce:\n\n"
            "1. Ad Concept\n"
            "   - Angle/theme (problem-aware, benefit-driven, social proof)\n"
            "   - Target audience segment\n"
            "   - Awareness level (cold/warm/hot)\n\n"
            "2. Primary Text (up to 125 characters visible + full text)\n"
            "   - Hook in first 125 characters (what shows before 'See More')\n"
            "   - Full ad copy (150-300 words)\n"
            "   - Format: short paragraphs, line breaks, emojis used sparingly\n\n"
            "3. Headline (max 40 characters)\n"
            "4. Description (max 30 characters)\n"
            "5. CTA Button recommendation (Learn More, Sign Up, Get Offer, etc.)\n\n"
            "6. Creative Direction\n"
            "   - Image/video concept recommendation\n"
            "   - Text overlay suggestions (max 20% image area)\n"
            "   - Format recommendation (single image, carousel, video)\n\n"
            "7. Targeting Notes\n"
            "   - Interest targeting suggestions\n"
            "   - Lookalike audience base recommendation\n"
            "   - Exclusion recommendations\n\n"
            "8. UTM Parameters for each variant\n\n"
            "Make each variant genuinely different in approach, not just rewording."
        )
        return await self.run(task=task, context=product_data, db=db, task_id=task_id)

    async def generate_linkedin_ads(
        self,
        product_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate LinkedIn Ads variants.

        Parameters
        ----------
        product_data : dict
            B2B product/service info, target titles/industries, USPs.
        """
        task = (
            "Create 3 LinkedIn Ad variants for a B2B audience.\n\n"
            "For each variant, produce:\n\n"
            "1. Ad Format\n"
            "   - Recommended format (single image, carousel, video, document)\n"
            "   - Placement (feed, right rail, message)\n\n"
            "2. Introductory Text (up to 150 characters visible + full text)\n"
            "   - Hook in first 150 characters\n"
            "   - Full text (150-300 words)\n"
            "   - Professional, B2B-focused tone\n"
            "   - Problem-aware messaging\n\n"
            "3. Headline (max 70 characters)\n"
            "4. Description (max 100 characters)\n"
            "5. CTA Button recommendation\n\n"
            "6. Creative Direction\n"
            "   - Image/visual concept\n"
            "   - Professional, B2B-appropriate style\n\n"
            "7. Targeting Recommendations\n"
            "   - Job titles, seniority levels\n"
            "   - Company size, industry\n"
            "   - Skills/interest targeting\n\n"
            "8. UTM Parameters\n\n"
            "LinkedIn tone: professional but not stuffy. Problem-aware, data-driven."
        )
        return await self.run(task=task, context=product_data, db=db, task_id=task_id)

    async def create_landing_page_copy(
        self,
        offer: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Create landing page copy and structure.

        Parameters
        ----------
        offer : dict
            The specific offer, target audience, traffic source, awareness level.
        """
        task = (
            "Create a complete landing page copy document.\n\n"
            "Structure:\n\n"
            "1. Above the Fold\n"
            "   - Headline: outcome-focused (what they get)\n"
            "   - Subheadline: mechanism (how it works)\n"
            "   - CTA button text + color recommendation\n"
            "   - Proof element (number, testimonial snippet, logo bar)\n"
            "   - Hero image/video direction\n\n"
            "2. Problem Section\n"
            "   - 3-4 pain points in their language\n"
            "   - 'Sound familiar?' bridge\n\n"
            "3. Solution Section\n"
            "   - How the engine/system solves their problem\n"
            "   - 3 key differentiators or features (with benefits)\n"
            "   - Process overview (3-4 steps: how it works)\n\n"
            "4. Social Proof Section\n"
            "   - Testimonial placement (what kind of proof to use)\n"
            "   - Metrics/results format\n"
            "   - Trust badges/logos\n"
            "   Note: Do NOT fabricate testimonials — use placeholders for real ones\n\n"
            "5. Objection Handling Section\n"
            "   - FAQ format addressing top 4-5 objections\n"
            "   - Each answer is concise and confidence-building\n\n"
            "6. Final CTA Section\n"
            "   - Urgency element (if appropriate)\n"
            "   - Risk reversal (guarantee, free audit, etc.)\n"
            "   - CTA button text (same as above-fold)\n"
            "   - Supporting copy below CTA\n\n"
            "7. Technical Notes\n"
            "   - Conversion tracking requirements\n"
            "   - Form fields recommendation\n"
            "   - Mobile optimization notes\n"
            "   - Page speed recommendations\n"
            "   - UTM handling\n\n"
            "Every element earns its place. No filler sections."
        )
        return await self.run(task=task, context=offer, db=db, task_id=task_id)

    async def design_ab_test_plan(
        self,
        campaign_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Design an A/B test plan for ad campaigns.

        Parameters
        ----------
        campaign_data : dict
            Current campaign performance, hypotheses, budget.
        """
        task = (
            "Design an A/B test roadmap for this ad campaign.\n\n"
            "Produce:\n\n"
            "1. Test Priority List (ordered by expected impact)\n"
            "   For each test:\n"
            "   - Test name\n"
            "   - Hypothesis ('We believe [change] will [effect] because [reason]')\n"
            "   - Variable to test (one variable only)\n"
            "   - Control vs. variant description\n"
            "   - Primary metric (CTR, CPA, conversion rate, etc.)\n"
            "   - Guardrail metrics (what we don't want to hurt)\n"
            "   - Minimum sample size / budget needed\n"
            "   - Estimated test duration\n"
            "   - Success criteria (e.g., '15% improvement in CTR')\n\n"
            "2. Test Schedule\n"
            "   - Which tests to run sequentially\n"
            "   - Which can run in parallel\n"
            "   - Dependencies between tests\n"
            "   - Total timeline\n\n"
            "3. Measurement Framework\n"
            "   - How to ensure statistical significance\n"
            "   - Tools for tracking (platform native, third-party)\n"
            "   - Reporting template for each test\n\n"
            "4. Decision Framework\n"
            "   - When to call a test (minimum confidence level)\n"
            "   - What to do with winners (scale, iterate, test next variable)\n"
            "   - What to do with losers (discard, iterate, test different approach)\n\n"
            "Recommend 5-8 tests, prioritized by expected revenue impact."
        )
        return await self.run(task=task, context=campaign_data, db=db, task_id=task_id)

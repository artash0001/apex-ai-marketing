"""
Apex AI Marketing - Agent 4: Local Visibility Agent

Model: Claude Sonnet
Engine: Local Visibility Engine
Language: both (EN + RU)

Manages Google Business Profile optimization, local citations,
review generation, and local content.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class LocalVisibilityAgent(BaseAgent):
    name = "Local Visibility Agent"
    role = (
        "Manages Google Business Profile optimization, local citations, "
        "review generation, and local content."
    )
    engine = "Local Visibility Engine"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.7
    max_tokens = 6144
    language = "both"

    system_prompt = (
        "You are a local search specialist. You make businesses dominate their local market "
        "in Google Maps and local search results.\n\n"
        "For each Local Visibility Engine client:\n"
        "1. GBP Audit (completeness score, optimization gaps, competitive comparison)\n"
        "2. Citation Strategy (which directories, NAP format, priority order)\n"
        "3. Review Generation System (request templates for email/SMS/WhatsApp, response templates)\n"
        "4. Local Content Plan (location-specific pages, local keyword targets)\n"
        "5. Monthly Report (ranking positions, GBP actions, review trends, citation health)\n\n"
        "You write content that sounds natural and local — not generic SEO-optimized filler.\n"
        "For Russian-speaking businesses in Dubai, you understand the local market nuances:\n"
        "- Many customers search in both English and Russian\n"
        "- Google Maps is primary, but Yandex Maps matters for Russian speakers\n"
        "- WhatsApp and Telegram are preferred communication channels in UAE\n"
        "- Review culture in Dubai is different — personal referrals carry more weight\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' 'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'\n\n"
        "Local SEO Knowledge:\n"
        "- Google Business Profile optimization (categories, attributes, photos, posts, Q&A)\n"
        "- Local pack ranking factors (relevance, distance, prominence)\n"
        "- Citation sources: general (Yelp, YP, Foursquare) + industry-specific + local (Dubai directories)\n"
        "- NAP consistency (Name, Address, Phone) across all listings\n"
        "- Review velocity and sentiment impact on rankings\n"
        "- Local schema markup (LocalBusiness, Organization)\n"
        "- GBP post types (updates, offers, events, products)\n\n"
        "Dubai/UAE Specific:\n"
        "- Key directories: Dubai Yellow Pages, UAE Business Directory, Bayut (real estate), Dubizzle\n"
        "- Russian directories: Russian Dubai, Dubai Russian Portal, RBC UAE listings\n"
        "- Google Maps dominates but Yandex Maps matters for Russian-speaking audience\n"
        "- Business hours: Sunday-Thursday standard, Friday/Saturday variable\n"
        "- Location formats: Dubai Marina, Business Bay, JLT, DIFC, etc."
    )

    async def audit_gbp(
        self,
        business_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Audit a Google Business Profile and provide optimization recommendations.

        Parameters
        ----------
        business_data : dict
            Business info including name, address, industry, current GBP status, competitors.
        """
        task = (
            "Perform a complete Google Business Profile audit for this business.\n\n"
            "Produce:\n\n"
            "1. Completeness Score (0-100%)\n"
            "   - Business info filled: name, address, phone, website, hours, description\n"
            "   - Categories: primary and secondary categories set correctly\n"
            "   - Attributes: relevant attributes enabled\n"
            "   - Photos: quantity, quality, types (exterior, interior, team, products)\n"
            "   - Posts: frequency, type, engagement\n"
            "   - Q&A: populated with common questions\n"
            "   - Products/Services: listed with descriptions and prices\n"
            "   - Reviews: count, rating, response rate, response quality\n\n"
            "2. Optimization Gaps\n"
            "   - Missing or incorrect information\n"
            "   - Underutilized features\n"
            "   - Category optimization opportunities\n"
            "   - Photo gaps (recommended types and quantities)\n"
            "   - Post strategy recommendations\n\n"
            "3. Competitive Comparison\n"
            "   - Compare against top 3 local competitors in Maps\n"
            "   - Review count and rating comparison\n"
            "   - Category and attribute comparison\n"
            "   - Photo and post activity comparison\n\n"
            "4. Priority Action Plan\n"
            "   - Immediate fixes (this week)\n"
            "   - Short-term improvements (this month)\n"
            "   - Ongoing optimization (monthly recurring)\n"
            "   - Expected impact of each action\n\n"
            "5. Monthly GBP Content Calendar\n"
            "   - Post topics and types by week\n"
            "   - Photo upload schedule\n"
            "   - Q&A additions\n"
            "   - Offer/event posts\n\n"
            "Format as an actionable audit document with specific steps and priorities."
        )
        return await self.run(task=task, context=business_data, db=db, task_id=task_id)

    async def create_citation_strategy(
        self,
        business_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Create a citation building and management strategy.

        Parameters
        ----------
        business_data : dict
            Business info including name, address, phone, industry, location, target market.
        """
        task = (
            "Create a comprehensive citation strategy for this business.\n\n"
            "Produce:\n\n"
            "1. NAP Format\n"
            "   - Exact business name format (consistent across all listings)\n"
            "   - Address format (standardized)\n"
            "   - Phone number format (with country code)\n"
            "   - Website URL format\n"
            "   - Additional NAP elements (email, hours, categories)\n\n"
            "2. Citation Directory List (prioritized)\n"
            "   Tier 1 — Must-have (first 2 weeks):\n"
            "   - Google Business Profile, Apple Maps, Bing Places, Facebook\n"
            "   - Industry-specific directories\n"
            "   - Location-specific directories\n\n"
            "   Tier 2 — Important (month 1):\n"
            "   - General directories (Yelp, YP, Foursquare, etc.)\n"
            "   - Industry aggregators\n"
            "   - Local chamber/association directories\n\n"
            "   Tier 3 — Nice-to-have (month 2-3):\n"
            "   - Niche directories, blog/resource mentions, partner listings\n\n"
            "   For Dubai businesses, include UAE-specific and Russian-language directories.\n\n"
            "3. Submission Checklist\n"
            "   - For each directory: URL, submission process, cost, timeline\n"
            "   - Account credentials management plan\n"
            "   - Verification requirements\n\n"
            "4. Monitoring Plan\n"
            "   - How to check citation consistency\n"
            "   - Tools for monitoring (manual + automated)\n"
            "   - Quarterly audit schedule\n"
            "   - Correction process for inconsistencies\n\n"
            "Format with clear priority tiers and specific directory names + URLs."
        )
        return await self.run(task=task, context=business_data, db=db, task_id=task_id)

    async def generate_review_templates(
        self,
        business_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate review request and response templates.

        Parameters
        ----------
        business_data : dict
            Business info including industry, service type,
            customer communication preferences, language.
        """
        task = (
            "Create a complete review generation system for this business.\n\n"
            "Produce:\n\n"
            "1. Review Request Templates\n"
            "   - Email template (post-service/purchase)\n"
            "   - SMS template (short, with direct link)\n"
            "   - WhatsApp template (conversational)\n"
            "   - In-person/QR code card copy\n"
            "   - Follow-up template (for non-responders, 3 days later)\n\n"
            "   For each template:\n"
            "   - Subject line (email) or opening line\n"
            "   - Body copy (personalized, specific, grateful)\n"
            "   - Direct review link placeholder\n"
            "   - Timing recommendation (when to send after service)\n\n"
            "2. Review Response Templates\n"
            "   - 5-star review response (3 variations)\n"
            "   - 4-star review response (2 variations)\n"
            "   - 3-star review response (2 variations — acknowledge, offer to improve)\n"
            "   - 1-2 star review response (2 variations — empathetic, solution-oriented, take offline)\n"
            "   - Fake/spam review response template\n\n"
            "   For each template:\n"
            "   - Thank the reviewer by name\n"
            "   - Reference specific service/product mentioned\n"
            "   - Keep professional but warm\n"
            "   - Never be defensive in negative review responses\n\n"
            "3. Review Generation Strategy\n"
            "   - Optimal timing for review requests per industry\n"
            "   - Frequency limits (don't spam customers)\n"
            "   - Review velocity target (reviews per week/month)\n"
            "   - Platform prioritization (Google first, then industry-specific)\n"
            "   - Employee training notes (how to ask in person)\n\n"
            "4. If bilingual (EN + RU):\n"
            "   - All templates in both English and Russian\n"
            "   - Russian templates should feel native, not translated\n"
            "   - Account for communication style differences\n\n"
            "Format as copy-paste ready templates with [PLACEHOLDER] fields clearly marked."
        )
        return await self.run(task=task, context=business_data, db=db, task_id=task_id)

    async def create_local_content(
        self,
        keywords: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Create local content plan and location-specific page copy.

        Parameters
        ----------
        keywords : dict
            Target keywords, locations, services, and audience info.
        """
        task = (
            "Create a local content plan with location-specific page recommendations.\n\n"
            "Produce:\n\n"
            "1. Local Keyword Map\n"
            "   - Service + location keyword combinations\n"
            "   - Search volume estimates or priority ranking\n"
            "   - Competitor difficulty assessment\n"
            "   - Intent classification (informational, commercial, transactional)\n\n"
            "2. Location Page Strategy\n"
            "   - Which location pages to create (area/neighborhood specific)\n"
            "   - Page structure template with unique local content requirements\n"
            "   - Local landmarks, neighborhoods, context\n"
            "   - Embedded map and location-specific testimonials\n"
            "   - Local schema markup specifications\n\n"
            "3. Local Blog Content Ideas (12 topics)\n"
            "   - Topic, target keyword, intent, content type\n"
            "   - Local angle for each topic\n"
            "   - Internal linking strategy to service/location pages\n\n"
            "4. GBP Post Content Calendar (4 weeks)\n"
            "   - Post type, topic, CTA for each week\n"
            "   - Photo/image recommendations\n"
            "   - Offer posts where appropriate\n\n"
            "5. For bilingual businesses:\n"
            "   - English and Russian content priorities\n"
            "   - Which pages need both languages\n"
            "   - Russian-specific keyword targets\n\n"
            "Format as a content calendar and implementation plan."
        )
        return await self.run(task=task, context=keywords, db=db, task_id=task_id)

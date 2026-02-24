"""
Apex AI Marketing - Agent 5: Content Engine Agent

Model: Claude Sonnet
Engine: Inbound Demand Engine
Language: both (EN + RU)

Creates SEO content that generates sales conversations —
topic maps, content briefs, articles, and AI-search readiness.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class ContentEngineAgent(BaseAgent):
    name = "Content Engine Agent"
    role = (
        "Creates SEO content that generates sales conversations — "
        "topic maps, content briefs, articles, and AI-search readiness."
    )
    engine = "Inbound Demand Engine"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.7
    max_tokens = 8192
    language = "both"

    system_prompt = (
        "You write content that ranks AND converts. You are not a content mill — "
        "you build content systems.\n\n"
        "When building an Inbound Demand Engine:\n"
        "1. Topic Map (organized by buyer journey stage, with keyword clusters)\n"
        "2. Content Briefs (keyword target, search intent, competitor analysis, "
        "recommended structure, word count, angle)\n"
        "3. Articles (SEO-optimized, outcome-focused, with clear CTAs)\n"
        "4. GEO/AEO Preparation (structured answers for AI search engines)\n\n"
        "Rules:\n"
        "- Every article starts with the reader's pain point, not the company's product\n"
        "- Use specific numbers, data, and examples — never vague\n"
        "- Write at 8th-grade reading level\n"
        "- Every H2 section should be independently scannable\n"
        "- Include a clear CTA tied to the client's engine (not generic 'learn more')\n"
        "- Short paragraphs (2-3 sentences max)\n"
        "- No buzzwords, no fluff, no filler content\n"
        "- For Russian-language content: write natively, don't translate — "
        "Russian business readers detect translated content immediately\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' "
        "'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'\n\n"
        "Content Structure Standards:\n"
        "- Title: Include primary keyword, benefit-driven, under 60 characters\n"
        "- Meta description: 150-160 characters, include keyword, include CTA\n"
        "- Introduction: Hook (pain point) → Context (why it matters) → Promise (what they'll learn)\n"
        "- Body: H2 sections with clear subtopics, each independently valuable\n"
        "- Conclusion: Summary → CTA → Next step\n"
        "- Internal links: 3-5 per article to relevant service/content pages\n"
        "- External links: 2-3 authoritative sources (only if they add genuine value)\n\n"
        "GEO/AEO Preparation:\n"
        "- Structure content with clear question-answer pairs\n"
        "- Use schema markup recommendations (FAQ, HowTo, Article)\n"
        "- Provide concise, direct answers in the first paragraph of each section\n"
        "- Include structured data recommendations for each article"
    )

    async def create_topic_map(
        self,
        client_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Create a comprehensive topic map organized by buyer journey stage.

        Parameters
        ----------
        client_data : dict
            Client info including industry, services, target audience,
            competitors, existing content.
        """
        task = (
            "Create a comprehensive topic map for this client's Inbound Demand Engine.\n\n"
            "Produce:\n\n"
            "1. Buyer Journey Mapping\n"
            "   - Awareness stage: Problems the buyer is experiencing\n"
            "   - Consideration stage: Buyer is evaluating solutions and approaches\n"
            "   - Decision stage: Buyer is comparing specific providers/products\n\n"
            "2. Keyword Clusters (organized by journey stage)\n"
            "   For each cluster:\n"
            "   - Primary keyword (highest value target)\n"
            "   - Secondary keywords (related terms, long-tail variations)\n"
            "   - Search intent (informational, commercial, transactional, navigational)\n"
            "   - Estimated difficulty (low, medium, high)\n"
            "   - Content type recommendation (guide, comparison, case study, tool, checklist)\n"
            "   - Priority score (1-5 based on business value + achievability)\n\n"
            "3. Content Pillars (3-5 main themes)\n"
            "   For each pillar:\n"
            "   - Pillar page topic and target keyword\n"
            "   - Cluster content pieces (8-15 supporting articles)\n"
            "   - Internal linking structure (how cluster connects to pillar)\n\n"
            "4. Content Calendar Recommendation\n"
            "   - Publishing cadence (articles per week/month)\n"
            "   - Priority order (which articles to write first)\n"
            "   - Seasonal/timely content opportunities\n"
            "   - Content refresh schedule for existing pages\n\n"
            "5. Competitive Content Gap Analysis\n"
            "   - Topics competitors rank for that client doesn't\n"
            "   - Content quality comparison\n"
            "   - Opportunities for better/more comprehensive content\n\n"
            "6. GEO/AEO Opportunity Map\n"
            "   - Topics where AI search engines frequently cite sources\n"
            "   - Question-based content opportunities\n"
            "   - Featured snippet targets\n\n"
            "Format as a structured document with clear tables and priority rankings."
        )
        return await self.run(task=task, context=client_data, db=db, task_id=task_id)

    async def generate_content_brief(
        self,
        topic: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Generate a detailed content brief for a specific article.

        Parameters
        ----------
        topic : dict
            Target keyword, intent, content type, buyer journey stage,
            and any specific requirements.
        """
        task = (
            "Generate a detailed content brief for this article topic.\n\n"
            "Produce:\n\n"
            "1. Article Overview\n"
            "   - Working title (3 options — benefit-driven, include primary keyword)\n"
            "   - Target keyword + secondary keywords\n"
            "   - Search intent and buyer journey stage\n"
            "   - Target word count and content type/format\n\n"
            "2. Competitor Analysis\n"
            "   - Top 3-5 currently ranking articles for this keyword\n"
            "   - What they cover well and what they miss (our opportunity)\n"
            "   - Average word count and format\n\n"
            "3. Recommended Structure\n"
            "   - H1 (title), introduction approach, H2/H3 sections with descriptions\n"
            "   - Conclusion approach and CTA recommendation\n\n"
            "4. Content Requirements\n"
            "   - Key points that MUST be covered\n"
            "   - Data/statistics to include (with source requirements)\n"
            "   - Examples or case study angles\n"
            "   - Internal/external linking targets\n"
            "   - Image/visual recommendations\n\n"
            "5. SEO Specifications\n"
            "   - Meta title (under 60 chars)\n"
            "   - Meta description (150-160 chars)\n"
            "   - URL slug recommendation\n"
            "   - Schema markup type\n"
            "   - Featured snippet optimization notes\n\n"
            "6. GEO/AEO Notes\n"
            "   - Key questions this article should directly answer\n"
            "   - Structured answer format recommendations\n"
            "   - FAQ schema opportunities\n\n"
            "7. Quality Checklist\n"
            "   - [ ] Starts with reader's pain point\n"
            "   - [ ] Specific numbers and data used\n"
            "   - [ ] 8th-grade reading level\n"
            "   - [ ] Every H2 independently scannable\n"
            "   - [ ] Clear, specific CTA\n"
            "   - [ ] Short paragraphs (2-3 sentences)\n"
            "   - [ ] No buzzwords or filler\n\n"
            "Format as a brief that a writer can follow to produce a high-quality article."
        )
        return await self.run(task=task, context=topic, db=db, task_id=task_id)

    async def write_article(
        self,
        brief: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Write a complete SEO article from a content brief.

        Parameters
        ----------
        brief : dict
            Content brief (output from generate_content_brief).
        """
        task = (
            "Write a complete SEO article based on this content brief.\n\n"
            "Requirements:\n"
            "- Follow the structure from the brief exactly\n"
            "- Write at 8th-grade reading level\n"
            "- Short paragraphs (2-3 sentences maximum)\n"
            "- Every H2 section should be independently scannable and valuable\n"
            "- Start with the reader's pain point, not the product\n"
            "- Use specific numbers, data, and examples\n"
            "- Include a clear, specific CTA (not generic 'learn more')\n"
            "- Include internal linking placeholders [INTERNAL LINK: page name]\n"
            "- Include image placement suggestions [IMAGE: description]\n"
            "- Write the meta title and meta description\n"
            "- Include FAQ section at the end (for schema markup)\n\n"
            "Style:\n"
            "- Direct, engineering-minded tone\n"
            "- Benefits over features\n"
            "- Concrete over abstract\n"
            "- Outcome-focused\n"
            "- No buzzwords: 'revolutionary,' 'game-changing,' 'cutting-edge,' "
            "'leverage,' 'synergy' are banned\n"
            "- No filler content — every sentence earns its place\n\n"
            "Format:\n"
            "---\n"
            "Meta Title: [title]\n"
            "Meta Description: [description]\n"
            "URL Slug: [slug]\n"
            "---\n\n"
            "[Full article in markdown format]\n\n"
            "---\n"
            "FAQ Section:\n"
            "Q: [question]\n"
            "A: [answer]\n"
            "..."
        )
        return await self.run(
            task=task,
            context={"additional_data": f"Content Brief:\n{brief}"},
            db=db,
            task_id=task_id,
        )

    async def optimize_for_geo_aeo(
        self,
        content: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Optimize existing content for GEO/AEO (AI search engines).

        Parameters
        ----------
        content : dict
            The article content and target keywords.
        """
        task = (
            "Optimize this content for AI search engines (GEO/AEO).\n\n"
            "Analyze the content and produce:\n\n"
            "1. Current GEO/AEO Readiness Score (0-100)\n"
            "   - Does it directly answer common questions?\n"
            "   - Is information structured for extraction?\n"
            "   - Are there clear, concise answer paragraphs?\n"
            "   - Does it use appropriate schema markup?\n\n"
            "2. Question Mapping\n"
            "   - List all questions this content could answer\n"
            "   - For each question: does the current content answer it clearly?\n"
            "   - Missing questions that should be addressed\n\n"
            "3. Structured Answer Optimization\n"
            "   - For each key question: write a concise, direct answer (2-3 sentences)\n"
            "   - Format for easy extraction by AI systems\n\n"
            "4. Schema Markup Recommendations\n"
            "   - Article schema, FAQ schema, HowTo schema (if applicable)\n"
            "   - Breadcrumb schema, Organization schema\n\n"
            "5. Revised Content\n"
            "   - Full revised article with GEO/AEO optimizations applied\n"
            "   - Changes marked with [GEO OPTIMIZATION] comments\n"
            "   - New FAQ section or expanded existing one\n\n"
            "6. Monitoring Plan\n"
            "   - How to track AI search visibility\n"
            "   - Key queries to monitor\n"
            "   - Tools and methods for tracking\n\n"
            "Format as an optimization report with the full revised content included."
        )
        return await self.run(
            task=task,
            context={"additional_data": f"Content:\n{content}"},
            db=db,
            task_id=task_id,
        )

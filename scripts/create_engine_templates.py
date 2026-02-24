#!/usr/bin/env python3
"""
Apex AI Marketing - Engine Deliverable Template Creator

Creates deliverable templates for all 8 growth engines.
Each engine has a set of standard deliverables with defined
types, cadences, and quality requirements.

These templates are stored in the database and used by the
content generation pipeline to know what to produce and when.

Usage:
    python scripts/create_engine_templates.py

Environment:
    Requires DATABASE_URL to be set or uses default from settings.
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ── Engine Deliverable Definitions ────────────────────────────────────────

ENGINE_TEMPLATES = {
    "content_engine": {
        "display_name": "Content Engine",
        "description": (
            "Authority-building content that drives organic traffic "
            "and establishes thought leadership."
        ),
        "deliverables": [
            {
                "type": "content_brief",
                "name": "SEO Content Brief",
                "description": (
                    "Detailed content brief with target keyword, search intent, "
                    "outline, competitor analysis, and word count guidance."
                ),
                "cadence": "weekly",
                "quantity_per_month": 8,
                "quality_threshold": 7.0,
                "ai_agent": "content_engine",
                "template_structure": {
                    "sections": [
                        "Target Keyword & Search Intent",
                        "Working Title Options (3)",
                        "Content Outline (H2/H3 structure)",
                        "Competitor Content Analysis (top 3 results)",
                        "Unique Angle / Value Proposition",
                        "Internal Linking Opportunities",
                        "Target Word Count",
                        "CTA Placement Strategy",
                    ],
                },
            },
            {
                "type": "article",
                "name": "SEO Article",
                "description": (
                    "Long-form, SEO-optimized article following the content brief. "
                    "Includes meta title, meta description, and alt text for images."
                ),
                "cadence": "weekly",
                "quantity_per_month": 4,
                "quality_threshold": 7.5,
                "ai_agent": "content_engine",
                "template_structure": {
                    "sections": [
                        "Meta Title (60 chars)",
                        "Meta Description (155 chars)",
                        "Article Body (structured with H2/H3)",
                        "Key Takeaways / Summary",
                        "Internal Links",
                        "CTA Section",
                        "Image Alt Text Suggestions",
                    ],
                },
            },
            {
                "type": "content_calendar",
                "name": "Monthly Content Calendar",
                "description": (
                    "Monthly content calendar aligned with keyword research, "
                    "seasonal trends, and business priorities."
                ),
                "cadence": "monthly",
                "quantity_per_month": 1,
                "quality_threshold": 7.0,
                "ai_agent": "content_engine",
                "template_structure": {
                    "sections": [
                        "Monthly Theme / Focus",
                        "Week-by-Week Content Plan",
                        "Keyword Targets per Piece",
                        "Content Format Mix",
                        "Distribution Plan",
                        "Performance Metrics to Track",
                    ],
                },
            },
        ],
    },
    "seo_engine": {
        "display_name": "SEO Architecture Engine",
        "description": (
            "Technical and on-page SEO that builds sustainable organic visibility."
        ),
        "deliverables": [
            {
                "type": "technical_audit",
                "name": "Technical SEO Audit",
                "description": "Comprehensive technical SEO audit with prioritized action items.",
                "cadence": "quarterly",
                "quantity_per_month": 0.33,
                "quality_threshold": 8.0,
                "ai_agent": "seo_architect",
                "template_structure": {
                    "sections": [
                        "Crawlability Analysis",
                        "Indexation Status",
                        "Page Speed Assessment",
                        "Mobile Usability",
                        "Schema Markup Audit",
                        "Internal Linking Structure",
                        "Canonical & Redirect Audit",
                        "Priority Action Items (ranked)",
                    ],
                },
            },
            {
                "type": "seo_page",
                "name": "On-Page Optimization Plan",
                "description": "Page-level SEO optimization recommendations for target pages.",
                "cadence": "weekly",
                "quantity_per_month": 4,
                "quality_threshold": 7.0,
                "ai_agent": "seo_architect",
                "template_structure": {
                    "sections": [
                        "Target Page URL",
                        "Primary & Secondary Keywords",
                        "Title Tag Recommendation",
                        "Meta Description",
                        "H1/H2 Structure",
                        "Content Additions / Changes",
                        "Internal Link Additions",
                        "Schema Markup Recommendations",
                    ],
                },
            },
            {
                "type": "keyword_report",
                "name": "Keyword Ranking Report",
                "description": "Monthly keyword ranking tracking and analysis.",
                "cadence": "monthly",
                "quantity_per_month": 1,
                "quality_threshold": 7.0,
                "ai_agent": "seo_architect",
                "template_structure": {
                    "sections": [
                        "Ranking Changes Summary",
                        "Top Gaining Keywords",
                        "Keywords Needing Attention",
                        "New Keyword Opportunities",
                        "Competitor Ranking Comparison",
                    ],
                },
            },
        ],
    },
    "paid_performance": {
        "display_name": "Paid Performance Engine",
        "description": "AI-optimized paid campaigns that improve weekly.",
        "deliverables": [
            {
                "type": "ad_copy",
                "name": "Ad Copy Set",
                "description": "Set of ad copy variants for A/B testing.",
                "cadence": "weekly",
                "quantity_per_month": 4,
                "quality_threshold": 7.0,
                "ai_agent": "paid_performance",
                "template_structure": {
                    "sections": [
                        "Campaign Objective",
                        "Target Audience Segment",
                        "Headlines (5 variants)",
                        "Descriptions (3 variants)",
                        "Call-to-Action Options",
                        "Landing Page Alignment Notes",
                    ],
                },
            },
            {
                "type": "campaign_report",
                "name": "Campaign Performance Report",
                "description": "Weekly campaign performance analysis with optimization actions.",
                "cadence": "weekly",
                "quantity_per_month": 4,
                "quality_threshold": 7.5,
                "ai_agent": "paid_performance",
                "template_structure": {
                    "sections": [
                        "Spend Summary",
                        "Key Metrics (CPC, CTR, Conv Rate, ROAS)",
                        "Top Performing Ads",
                        "Underperforming Ads",
                        "Audience Insights",
                        "Optimization Actions Taken",
                        "Next Week Plan",
                    ],
                },
            },
            {
                "type": "audience_analysis",
                "name": "Audience Analysis",
                "description": "Monthly audience performance analysis and targeting recommendations.",
                "cadence": "monthly",
                "quantity_per_month": 1,
                "quality_threshold": 7.0,
                "ai_agent": "paid_performance",
                "template_structure": {
                    "sections": [
                        "Audience Segment Performance",
                        "Demographic Insights",
                        "Behavioral Patterns",
                        "Lookalike Recommendations",
                        "Retargeting Strategy Updates",
                    ],
                },
            },
        ],
    },
    "social_media": {
        "display_name": "Social Media Engine",
        "description": "Brand presence and community building across platforms.",
        "deliverables": [
            {
                "type": "social_post",
                "name": "Social Media Post",
                "description": "Platform-optimized social media post with copy and hashtags.",
                "cadence": "daily",
                "quantity_per_month": 20,
                "quality_threshold": 6.5,
                "ai_agent": "social_media",
                "template_structure": {
                    "sections": [
                        "Platform (Instagram/LinkedIn/Facebook/X)",
                        "Post Type (carousel, single, reel script, story)",
                        "Caption / Copy",
                        "Hashtag Strategy",
                        "Visual Direction Notes",
                        "Best Posting Time",
                    ],
                },
            },
            {
                "type": "social_calendar",
                "name": "Social Media Calendar",
                "description": "Monthly social content calendar with themes and cadence.",
                "cadence": "monthly",
                "quantity_per_month": 1,
                "quality_threshold": 7.0,
                "ai_agent": "social_media",
                "template_structure": {
                    "sections": [
                        "Monthly Theme",
                        "Platform-Specific Plans",
                        "Content Mix (value/promo/engagement)",
                        "Key Dates & Events",
                        "Engagement Strategy",
                    ],
                },
            },
            {
                "type": "social_report",
                "name": "Social Media Performance Report",
                "description": "Monthly social media analytics and insights.",
                "cadence": "monthly",
                "quantity_per_month": 1,
                "quality_threshold": 7.0,
                "ai_agent": "social_media",
                "template_structure": {
                    "sections": [
                        "Follower Growth",
                        "Engagement Metrics",
                        "Top Performing Posts",
                        "Audience Demographics",
                        "Competitor Benchmarking",
                        "Recommendations",
                    ],
                },
            },
        ],
    },
    "email_nurture": {
        "display_name": "Email Nurture Engine",
        "description": "Lead nurturing and customer retention through email sequences.",
        "deliverables": [
            {
                "type": "email_sequence",
                "name": "Email Sequence",
                "description": "Automated email sequence for a specific segment or trigger.",
                "cadence": "monthly",
                "quantity_per_month": 2,
                "quality_threshold": 7.5,
                "ai_agent": "email_sequence_builder",
                "template_structure": {
                    "sections": [
                        "Sequence Name & Trigger",
                        "Target Segment",
                        "Email 1: Subject + Body + CTA",
                        "Email 2: Subject + Body + CTA",
                        "Email 3: Subject + Body + CTA",
                        "Delay Timing Between Emails",
                        "Exit Conditions",
                    ],
                },
            },
            {
                "type": "newsletter",
                "name": "Newsletter",
                "description": "Monthly newsletter content for the subscriber base.",
                "cadence": "monthly",
                "quantity_per_month": 1,
                "quality_threshold": 7.0,
                "ai_agent": "email_sequence_builder",
                "template_structure": {
                    "sections": [
                        "Subject Line (3 options for A/B test)",
                        "Preview Text",
                        "Header Section",
                        "Main Content Blocks (3-5)",
                        "CTA Sections",
                        "Footer / PS Line",
                    ],
                },
            },
            {
                "type": "email_report",
                "name": "Email Performance Report",
                "description": "Monthly email marketing performance analysis.",
                "cadence": "monthly",
                "quantity_per_month": 1,
                "quality_threshold": 7.0,
                "ai_agent": "email_sequence_builder",
                "template_structure": {
                    "sections": [
                        "List Growth",
                        "Open Rates by Segment",
                        "Click Rates",
                        "Conversion Attribution",
                        "A/B Test Results",
                        "Deliverability Health",
                    ],
                },
            },
        ],
    },
    "local_visibility": {
        "display_name": "Local Visibility Engine",
        "description": "Dominate local search and directory presence.",
        "deliverables": [
            {
                "type": "gmb_post",
                "name": "Google Business Profile Post",
                "description": "Weekly GBP post for local engagement and visibility.",
                "cadence": "weekly",
                "quantity_per_month": 4,
                "quality_threshold": 6.5,
                "ai_agent": "local_visibility",
                "template_structure": {
                    "sections": [
                        "Post Type (Update/Offer/Event)",
                        "Post Copy",
                        "CTA Button",
                        "Image Direction",
                    ],
                },
            },
            {
                "type": "review_response",
                "name": "Review Response Templates",
                "description": "Templates for responding to Google reviews.",
                "cadence": "monthly",
                "quantity_per_month": 1,
                "quality_threshold": 7.0,
                "ai_agent": "local_visibility",
                "template_structure": {
                    "sections": [
                        "5-Star Review Response (3 variants)",
                        "4-Star Review Response (2 variants)",
                        "3-Star Review Response (2 variants)",
                        "Negative Review Response Framework",
                        "Review Request Email/SMS Template",
                    ],
                },
            },
            {
                "type": "local_seo_report",
                "name": "Local Visibility Report",
                "description": "Monthly local SEO and GBP performance report.",
                "cadence": "monthly",
                "quantity_per_month": 1,
                "quality_threshold": 7.0,
                "ai_agent": "local_visibility",
                "template_structure": {
                    "sections": [
                        "GBP Insights Summary",
                        "Local Pack Rankings",
                        "Review Metrics",
                        "Directory Listing Audit",
                        "Local Keyword Rankings",
                        "Competitor Local Comparison",
                    ],
                },
            },
        ],
    },
    "conversion_optimization": {
        "display_name": "Conversion Optimization Engine",
        "description": "Systematic improvement of website conversion rates.",
        "deliverables": [
            {
                "type": "conversion_audit",
                "name": "Conversion Audit",
                "description": "Detailed analysis of conversion funnel with heatmap insights.",
                "cadence": "quarterly",
                "quantity_per_month": 0.33,
                "quality_threshold": 8.0,
                "ai_agent": "conversion_optimizer",
                "template_structure": {
                    "sections": [
                        "Funnel Map (stages and drop-off rates)",
                        "Heatmap Analysis (key pages)",
                        "Form Analysis",
                        "CTA Effectiveness",
                        "Mobile vs Desktop Conversion",
                        "Speed Impact on Conversion",
                        "Priority Optimization Opportunities",
                    ],
                },
            },
            {
                "type": "landing_page",
                "name": "Landing Page Copy",
                "description": "High-converting landing page copy and structure.",
                "cadence": "monthly",
                "quantity_per_month": 2,
                "quality_threshold": 7.5,
                "ai_agent": "conversion_optimizer",
                "template_structure": {
                    "sections": [
                        "Headline & Sub-headline",
                        "Hero Section Copy",
                        "Problem / Agitation / Solution",
                        "Social Proof Section",
                        "Feature / Benefit Blocks",
                        "FAQ Section",
                        "CTA Sections (primary + secondary)",
                        "Trust Elements",
                    ],
                },
            },
            {
                "type": "ab_test_plan",
                "name": "A/B Test Plan",
                "description": "Structured A/B test design with hypothesis and metrics.",
                "cadence": "bi-weekly",
                "quantity_per_month": 2,
                "quality_threshold": 7.5,
                "ai_agent": "conversion_optimizer",
                "template_structure": {
                    "sections": [
                        "Hypothesis Statement",
                        "Variable Being Tested",
                        "Control vs Variant Description",
                        "Primary Metric",
                        "Guardrail Metrics",
                        "Required Sample Size",
                        "Expected Duration",
                        "Success Criteria",
                    ],
                },
            },
        ],
    },
    "growth_ops": {
        "display_name": "Growth Ops Engine",
        "description": (
            "Strategic layer coordinating all engines and driving compounding growth."
        ),
        "deliverables": [
            {
                "type": "growth_roadmap",
                "name": "Growth Roadmap",
                "description": "Quarterly strategic growth roadmap with milestones.",
                "cadence": "quarterly",
                "quantity_per_month": 0.33,
                "quality_threshold": 8.5,
                "ai_agent": "strategy_architect",
                "template_structure": {
                    "sections": [
                        "Quarterly Objectives",
                        "Engine Coordination Plan",
                        "Experiment Pipeline",
                        "KPI Targets by Month",
                        "Risk Assessment",
                        "Resource Allocation",
                        "Milestone Timeline",
                    ],
                },
            },
            {
                "type": "experiment_proposal",
                "name": "Experiment Proposal",
                "description": "Structured experiment proposal with hypothesis and design.",
                "cadence": "weekly",
                "quantity_per_month": 4,
                "quality_threshold": 7.5,
                "ai_agent": "strategy_architect",
                "template_structure": {
                    "sections": [
                        "Hypothesis",
                        "Variable Changed",
                        "Primary Metric",
                        "Guardrail Metrics",
                        "Test Design",
                        "Duration & Sample Size",
                        "Expected Impact",
                        "Resource Requirements",
                    ],
                },
            },
            {
                "type": "cross_engine_report",
                "name": "Cross-Engine Performance Report",
                "description": "Monthly report analyzing how engines work together.",
                "cadence": "monthly",
                "quantity_per_month": 1,
                "quality_threshold": 8.0,
                "ai_agent": "strategy_architect",
                "template_structure": {
                    "sections": [
                        "Engine Synergy Analysis",
                        "Attribution Model Results",
                        "Compound Growth Indicators",
                        "Bottleneck Identification",
                        "Optimization Recommendations",
                        "Next Month Priorities",
                    ],
                },
            },
        ],
    },
}


async def create_engine_templates():
    """Insert all engine deliverable templates into the database."""
    from backend.database import async_session_factory, init_db

    await init_db()

    async with async_session_factory() as session:
        from sqlalchemy import text

        # Create engine_templates table
        await session.execute(text("""
            CREATE TABLE IF NOT EXISTS engine_deliverable_templates (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                engine_key VARCHAR(100) NOT NULL,
                engine_display_name VARCHAR(255) NOT NULL,
                engine_description TEXT,
                deliverable_type VARCHAR(100) NOT NULL,
                deliverable_name VARCHAR(255) NOT NULL,
                deliverable_description TEXT,
                cadence VARCHAR(50) NOT NULL,
                quantity_per_month REAL NOT NULL DEFAULT 1,
                quality_threshold REAL NOT NULL DEFAULT 7.0,
                ai_agent VARCHAR(100) NOT NULL,
                template_structure JSONB DEFAULT '{}'::jsonb,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(engine_key, deliverable_type)
            )
        """))
        await session.commit()

        total_created = 0

        for engine_key, engine_data in ENGINE_TEMPLATES.items():
            deliverable_count = 0

            for deliverable in engine_data["deliverables"]:
                await session.execute(text("""
                    INSERT INTO engine_deliverable_templates
                        (engine_key, engine_display_name, engine_description,
                         deliverable_type, deliverable_name, deliverable_description,
                         cadence, quantity_per_month, quality_threshold,
                         ai_agent, template_structure)
                    VALUES
                        (:engine_key, :display_name, :description,
                         :del_type, :del_name, :del_description,
                         :cadence, :quantity, :threshold,
                         :agent, :structure)
                    ON CONFLICT (engine_key, deliverable_type) DO UPDATE SET
                        deliverable_name = EXCLUDED.deliverable_name,
                        deliverable_description = EXCLUDED.deliverable_description,
                        cadence = EXCLUDED.cadence,
                        quantity_per_month = EXCLUDED.quantity_per_month,
                        quality_threshold = EXCLUDED.quality_threshold,
                        ai_agent = EXCLUDED.ai_agent,
                        template_structure = EXCLUDED.template_structure,
                        updated_at = NOW()
                """), {
                    "engine_key": engine_key,
                    "display_name": engine_data["display_name"],
                    "description": engine_data["description"],
                    "del_type": deliverable["type"],
                    "del_name": deliverable["name"],
                    "del_description": deliverable["description"],
                    "cadence": deliverable["cadence"],
                    "quantity": deliverable["quantity_per_month"],
                    "threshold": deliverable["quality_threshold"],
                    "agent": deliverable["ai_agent"],
                    "structure": json.dumps(deliverable["template_structure"]),
                })
                deliverable_count += 1
                total_created += 1

            print(
                f"  {engine_data['display_name']}: "
                f"{deliverable_count} deliverable templates"
            )

        await session.commit()

        print()
        print(f"Total templates created/updated: {total_created}")
        print(f"Engines configured: {len(ENGINE_TEMPLATES)}")

        # Print summary table
        print()
        print("Engine Deliverable Summary:")
        print("-" * 70)
        print(f"{'Engine':<30} {'Deliverables':<15} {'Monthly Output'}")
        print("-" * 70)

        for engine_key, engine_data in ENGINE_TEMPLATES.items():
            del_count = len(engine_data["deliverables"])
            monthly_output = sum(
                d["quantity_per_month"] for d in engine_data["deliverables"]
            )
            print(
                f"{engine_data['display_name']:<30} "
                f"{del_count:<15} "
                f"{monthly_output:.1f} items/month"
            )

        print("-" * 70)
        total_monthly = sum(
            sum(d["quantity_per_month"] for d in e["deliverables"])
            for e in ENGINE_TEMPLATES.values()
        )
        total_types = sum(len(e["deliverables"]) for e in ENGINE_TEMPLATES.values())
        print(f"{'TOTAL':<30} {total_types:<15} {total_monthly:.1f} items/month")


def main():
    """Entry point."""
    print("Apex AI Marketing - Engine Deliverable Template Creator")
    print("=" * 60)
    print()
    print("Creating deliverable templates for all 8 engines...")
    print()

    try:
        asyncio.run(create_engine_templates())
    except Exception as exc:
        print(f"\nError: {exc}")
        print()
        print("Make sure the database is running and DATABASE_URL is configured.")
        sys.exit(1)

    print()
    print("=" * 60)
    print("All engine templates created successfully.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Apex AI Marketing - Methodology Showcase & Benchmark Data Seeder

Generates sample data that demonstrates the agency's methodology and
analytical capabilities. This is NOT fake case studies or fabricated
results -- it is benchmark analysis data and methodology documentation.

Creates:
  1. Growth Infrastructure Methodology documentation
  2. Industry benchmark datasets for Dubai market
  3. Engine configuration templates with expected outcomes
  4. Audit scoring rubrics
  5. Experiment framework templates

Usage:
    python scripts/seed_proof.py
"""

import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "methodology"


def ensure_dirs():
    """Create data directories if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "benchmarks").mkdir(exist_ok=True)
    (DATA_DIR / "frameworks").mkdir(exist_ok=True)
    (DATA_DIR / "rubrics").mkdir(exist_ok=True)


def seed_methodology_framework():
    """Create the Growth Infrastructure Methodology documentation."""
    methodology = {
        "name": "Apex Growth Infrastructure Methodology",
        "version": "2.0",
        "last_updated": date.today().isoformat(),
        "core_philosophy": (
            "Marketing should operate as infrastructure -- integrated systems "
            "that compound over time -- not as disconnected campaigns with "
            "unpredictable outcomes."
        ),
        "three_pillars": {
            "ai_powered_execution": {
                "description": (
                    "Claude-based AI agents handle research, content generation, "
                    "optimization, and analysis at speed and consistency that "
                    "human teams alone cannot achieve."
                ),
                "key_capabilities": [
                    "Multi-language content generation (EN/RU)",
                    "Real-time performance analysis and optimization",
                    "Automated quality assurance with human oversight",
                    "Structured experiment design and evaluation",
                ],
            },
            "structured_experimentation": {
                "description": (
                    "Every marketing action is treated as a hypothesis. We measure, "
                    "learn, and iterate weekly. No guesswork, no vanity metrics."
                ),
                "experiment_framework": {
                    "steps": [
                        "Hypothesis formation with measurable prediction",
                        "Variable identification and control setup",
                        "Primary metric and guardrail metric definition",
                        "Execution period (typically 2 weeks)",
                        "Data collection and statistical analysis",
                        "Decision: implement, iterate, or discard",
                        "Learning documentation for institutional knowledge",
                    ],
                    "cadence": "Weekly review, bi-weekly new experiments",
                },
            },
            "transparent_reporting": {
                "description": (
                    "Clients see exactly what is happening, what is working, and "
                    "why. No black boxes, no vague metrics."
                ),
                "reporting_cadence": {
                    "real_time": "Telegram notifications for important events",
                    "weekly": "Full performance report with KPI tracking",
                    "monthly": "Comprehensive review with ROI analysis and billing",
                    "quarterly": "Strategic review and roadmap adjustment",
                },
            },
        },
        "engine_model": {
            "description": (
                "Each 'engine' is a self-contained growth system focused on "
                "a specific outcome. Engines run continuously, learning and "
                "improving. They are not projects with end dates -- they are "
                "infrastructure that compounds."
            ),
            "engines": [
                {
                    "name": "Content Engine",
                    "purpose": "Authority-building content that drives organic traffic and establishes thought leadership",
                    "typical_deliverables": [
                        "4-8 SEO-optimized articles per month",
                        "Content calendar aligned with search demand",
                        "Topic cluster strategy",
                        "Content performance tracking",
                    ],
                },
                {
                    "name": "SEO Architecture Engine",
                    "purpose": "Technical and on-page SEO that builds sustainable organic visibility",
                    "typical_deliverables": [
                        "Technical SEO audit and fixes",
                        "On-page optimization for target pages",
                        "Schema markup implementation",
                        "Monthly ranking and visibility reports",
                    ],
                },
                {
                    "name": "Paid Performance Engine",
                    "purpose": "AI-optimized paid campaigns that improve weekly",
                    "typical_deliverables": [
                        "Campaign setup and management (Google, Meta)",
                        "Weekly A/B testing of ads and audiences",
                        "Conversion tracking and attribution",
                        "ROAS optimization",
                    ],
                },
                {
                    "name": "Social Media Engine",
                    "purpose": "Brand presence and community building across platforms",
                    "typical_deliverables": [
                        "12-20 posts per month across platforms",
                        "Community engagement management",
                        "Hashtag and trend strategy",
                        "Platform-specific content optimization",
                    ],
                },
                {
                    "name": "Email Nurture Engine",
                    "purpose": "Lead nurturing and customer retention through email sequences",
                    "typical_deliverables": [
                        "Automated email sequences",
                        "Newsletter content",
                        "Segmentation strategy",
                        "A/B testing of subjects and content",
                    ],
                },
                {
                    "name": "Local Visibility Engine",
                    "purpose": "Dominate local search and directory presence",
                    "typical_deliverables": [
                        "Google Business Profile optimization",
                        "Directory listing management",
                        "Review generation strategy",
                        "Local content creation",
                    ],
                },
                {
                    "name": "Conversion Optimization Engine",
                    "purpose": "Systematic improvement of website conversion rates",
                    "typical_deliverables": [
                        "Conversion audit and heatmap analysis",
                        "Landing page optimization",
                        "A/B testing program",
                        "Funnel analysis and leak detection",
                    ],
                },
                {
                    "name": "Growth Ops Engine",
                    "purpose": "Strategic layer that coordinates all engines and drives compounding growth",
                    "typical_deliverables": [
                        "Growth strategy and roadmap",
                        "Cross-engine optimization",
                        "Experiment design and analysis",
                        "Quarterly strategic reviews",
                    ],
                },
            ],
        },
        "quality_assurance": {
            "process": [
                "AI agent generates initial deliverable",
                "Brand Voice Agent checks tone and terminology consistency",
                "Quality Gate scores on 4 dimensions (completeness, accuracy, actionability, formatting)",
                "Combined score >= 7/10 passes to human review",
                "Human review for strategic alignment and nuance",
                "Client delivery with revision cycle if needed",
            ],
            "max_iterations": 5,
            "escalation_trigger": "Score below 5/10 or 3+ iteration cycles",
        },
    }

    output_path = DATA_DIR / "growth_infrastructure_methodology.json"
    with open(output_path, "w") as f:
        json.dump(methodology, f, indent=2, ensure_ascii=False)

    print(f"  Methodology framework: {output_path}")
    return methodology


def seed_industry_benchmarks():
    """Create industry benchmark datasets for Dubai market."""
    benchmarks = {
        "market": "Dubai / UAE",
        "last_updated": date.today().isoformat(),
        "source_note": (
            "Benchmarks compiled from public industry reports, "
            "Google Ads benchmarking data, and aggregated analytics. "
            "These are reference ranges, not guarantees."
        ),
        "industries": {
            "real_estate": {
                "label": "Real Estate (Dubai)",
                "website": {
                    "avg_bounce_rate": "45-65%",
                    "avg_session_duration": "1:30-3:00",
                    "avg_pages_per_session": "2.5-4.0",
                    "mobile_traffic_share": "65-75%",
                },
                "seo": {
                    "avg_domain_authority": "15-35 (small agencies), 40-60 (established)",
                    "avg_organic_traffic_monthly": "500-5,000 (small), 10,000-50,000 (established)",
                    "top_keywords_competition": "High",
                    "local_pack_importance": "Critical",
                },
                "paid_advertising": {
                    "avg_cpc_google": "$1.50-$4.50",
                    "avg_cpc_meta": "$0.50-$2.00",
                    "avg_conversion_rate": "2-5%",
                    "avg_cost_per_lead": "$15-$60",
                    "avg_roas": "3x-8x",
                },
                "social_media": {
                    "avg_engagement_rate_instagram": "1.5-4%",
                    "avg_engagement_rate_linkedin": "2-5%",
                    "posting_frequency_recommended": "5-7x/week Instagram, 3-5x/week LinkedIn",
                },
                "email": {
                    "avg_open_rate": "18-28%",
                    "avg_click_rate": "2-5%",
                    "avg_unsubscribe_rate": "0.2-0.5%",
                },
            },
            "hospitality": {
                "label": "Hospitality & Tourism (Dubai)",
                "website": {
                    "avg_bounce_rate": "35-55%",
                    "avg_session_duration": "2:00-4:00",
                    "mobile_traffic_share": "70-80%",
                },
                "paid_advertising": {
                    "avg_cpc_google": "$0.80-$3.00",
                    "avg_conversion_rate": "3-7%",
                    "avg_cost_per_booking": "$10-$40",
                },
                "social_media": {
                    "avg_engagement_rate_instagram": "2-6%",
                    "visual_content_importance": "Critical",
                },
            },
            "professional_services": {
                "label": "Professional Services (Dubai)",
                "website": {
                    "avg_bounce_rate": "40-60%",
                    "avg_session_duration": "1:45-3:30",
                    "mobile_traffic_share": "55-65%",
                },
                "seo": {
                    "avg_domain_authority": "10-25 (new), 30-50 (established)",
                    "content_importance": "High (thought leadership)",
                },
                "paid_advertising": {
                    "avg_cpc_google": "$2.00-$8.00",
                    "avg_conversion_rate": "2-4%",
                    "avg_cost_per_lead": "$30-$120",
                },
                "email": {
                    "avg_open_rate": "20-30%",
                    "avg_click_rate": "2-4%",
                },
            },
            "ecommerce": {
                "label": "E-Commerce (UAE)",
                "website": {
                    "avg_bounce_rate": "30-50%",
                    "avg_session_duration": "2:00-5:00",
                    "mobile_traffic_share": "70-80%",
                    "avg_cart_abandonment_rate": "65-80%",
                },
                "paid_advertising": {
                    "avg_cpc_google_shopping": "$0.30-$1.50",
                    "avg_conversion_rate": "1.5-3.5%",
                    "avg_roas": "4x-12x",
                },
                "email": {
                    "avg_open_rate": "15-25%",
                    "avg_revenue_per_email": "$0.05-$0.20",
                },
            },
        },
    }

    output_path = DATA_DIR / "benchmarks" / "dubai_market_benchmarks.json"
    with open(output_path, "w") as f:
        json.dump(benchmarks, f, indent=2, ensure_ascii=False)

    print(f"  Industry benchmarks: {output_path}")
    return benchmarks


def seed_audit_scoring_rubric():
    """Create the audit scoring rubric used by the Infrastructure Auditor."""
    rubric = {
        "name": "Growth Infrastructure Audit Scoring Rubric",
        "version": "2.0",
        "total_possible_score": 100,
        "categories": {
            "website_technical": {
                "weight": 20,
                "criteria": {
                    "page_speed": {
                        "max_score": 5,
                        "scoring": {
                            "5": "LCP < 2.5s, FID < 100ms, CLS < 0.1",
                            "3": "LCP < 4s, FID < 300ms, CLS < 0.25",
                            "1": "LCP > 4s or FID > 300ms or CLS > 0.25",
                        },
                    },
                    "mobile_responsive": {
                        "max_score": 5,
                        "scoring": {
                            "5": "Fully responsive, excellent mobile UX",
                            "3": "Responsive but with minor issues",
                            "1": "Not mobile-friendly or major issues",
                        },
                    },
                    "ssl_security": {
                        "max_score": 3,
                        "scoring": {
                            "3": "Valid SSL, HSTS, secure forms",
                            "1": "SSL present but misconfigured",
                            "0": "No SSL or expired certificate",
                        },
                    },
                    "conversion_elements": {
                        "max_score": 5,
                        "scoring": {
                            "5": "Clear CTAs, lead capture, trust elements, chat",
                            "3": "Basic CTAs and contact forms present",
                            "1": "Minimal or no conversion architecture",
                        },
                    },
                    "analytics_tracking": {
                        "max_score": 2,
                        "scoring": {
                            "2": "GA4 + GTM + conversion tracking configured",
                            "1": "Basic analytics only",
                            "0": "No analytics installed",
                        },
                    },
                },
            },
            "seo_organic": {
                "weight": 20,
                "criteria": {
                    "technical_seo": {
                        "max_score": 5,
                        "scoring": {
                            "5": "Clean crawlability, proper indexing, schema markup",
                            "3": "Minor technical issues but functional",
                            "1": "Major crawlability or indexing problems",
                        },
                    },
                    "on_page_optimization": {
                        "max_score": 5,
                        "scoring": {
                            "5": "Optimized titles, metas, headers, internal linking",
                            "3": "Partially optimized",
                            "1": "No meaningful on-page SEO",
                        },
                    },
                    "backlink_authority": {
                        "max_score": 5,
                        "scoring": {
                            "5": "Strong, diverse backlink profile (DA 40+)",
                            "3": "Moderate authority (DA 20-40)",
                            "1": "Weak or no backlink profile (DA < 20)",
                        },
                    },
                    "keyword_targeting": {
                        "max_score": 5,
                        "scoring": {
                            "5": "Clear keyword strategy with ranking positions",
                            "3": "Some keyword targeting but not systematic",
                            "1": "No keyword strategy evident",
                        },
                    },
                },
            },
            "content": {
                "weight": 15,
                "criteria": {
                    "content_quantity": {
                        "max_score": 4,
                        "scoring": {
                            "4": "Regular publishing cadence, substantial library",
                            "2": "Sporadic content, thin library",
                            "0": "No blog or content marketing",
                        },
                    },
                    "content_quality": {
                        "max_score": 4,
                        "scoring": {
                            "4": "Original, in-depth, audience-focused content",
                            "2": "Generic or thin content",
                            "0": "No meaningful content",
                        },
                    },
                    "content_strategy": {
                        "max_score": 4,
                        "scoring": {
                            "4": "Topic clusters, funnel stages, clear strategy",
                            "2": "Some thematic consistency",
                            "0": "No visible content strategy",
                        },
                    },
                    "content_distribution": {
                        "max_score": 3,
                        "scoring": {
                            "3": "Multi-channel distribution, repurposing",
                            "1": "Published but not distributed",
                            "0": "No distribution strategy",
                        },
                    },
                },
            },
            "social_community": {
                "weight": 10,
                "criteria": {
                    "platform_presence": {"max_score": 3},
                    "engagement_rate": {"max_score": 4},
                    "posting_consistency": {"max_score": 3},
                },
            },
            "paid_advertising": {
                "weight": 15,
                "criteria": {
                    "campaign_structure": {"max_score": 5},
                    "targeting_quality": {"max_score": 5},
                    "conversion_tracking": {"max_score": 3},
                    "roas_efficiency": {"max_score": 5},
                },
            },
            "local_visibility": {
                "weight": 10,
                "criteria": {
                    "gmb_optimization": {"max_score": 5},
                    "review_profile": {"max_score": 3},
                    "directory_listings": {"max_score": 2},
                },
            },
            "competitive_position": {
                "weight": 10,
                "criteria": {
                    "market_differentiation": {"max_score": 5},
                    "share_of_voice": {"max_score": 5},
                },
            },
        },
    }

    output_path = DATA_DIR / "rubrics" / "audit_scoring_rubric.json"
    with open(output_path, "w") as f:
        json.dump(rubric, f, indent=2, ensure_ascii=False)

    print(f"  Audit scoring rubric: {output_path}")
    return rubric


def seed_experiment_frameworks():
    """Create experiment framework templates."""
    frameworks = {
        "experiment_types": [
            {
                "type": "headline_test",
                "category": "Conversion Optimization",
                "template": {
                    "hypothesis": (
                        "Changing the headline from '{control}' to '{variant}' "
                        "will increase {metric} by {expected_lift}% because {reasoning}."
                    ),
                    "typical_duration_days": 14,
                    "minimum_sample_size": 500,
                    "primary_metrics": ["click_through_rate", "conversion_rate"],
                    "guardrail_metrics": ["bounce_rate", "time_on_page"],
                },
            },
            {
                "type": "cta_test",
                "category": "Conversion Optimization",
                "template": {
                    "hypothesis": (
                        "Changing the CTA from '{control}' to '{variant}' "
                        "will increase click-through rate by {expected_lift}%."
                    ),
                    "typical_duration_days": 14,
                    "minimum_sample_size": 1000,
                    "primary_metrics": ["cta_click_rate"],
                    "guardrail_metrics": ["conversion_rate", "bounce_rate"],
                },
            },
            {
                "type": "ad_creative_test",
                "category": "Paid Performance",
                "template": {
                    "hypothesis": (
                        "Ad creative variant with {change_description} will "
                        "achieve {expected_lift}% higher CTR while maintaining "
                        "conversion rate within 5% of current levels."
                    ),
                    "typical_duration_days": 7,
                    "minimum_spend": "$200 per variant",
                    "primary_metrics": ["ctr", "cpc"],
                    "guardrail_metrics": ["conversion_rate", "cost_per_conversion"],
                },
            },
            {
                "type": "email_subject_test",
                "category": "Email Nurture",
                "template": {
                    "hypothesis": (
                        "Subject line '{variant}' will achieve {expected_lift}% "
                        "higher open rate than '{control}' for the {segment} segment."
                    ),
                    "typical_duration_days": 3,
                    "minimum_sample_size": 200,
                    "primary_metrics": ["open_rate"],
                    "guardrail_metrics": ["unsubscribe_rate", "spam_rate"],
                },
            },
            {
                "type": "landing_page_layout",
                "category": "Conversion Optimization",
                "template": {
                    "hypothesis": (
                        "Moving {element} from {position_a} to {position_b} "
                        "will increase form submissions by {expected_lift}%."
                    ),
                    "typical_duration_days": 21,
                    "minimum_sample_size": 500,
                    "primary_metrics": ["form_submission_rate"],
                    "guardrail_metrics": ["bounce_rate", "scroll_depth"],
                },
            },
            {
                "type": "content_format_test",
                "category": "Content Engine",
                "template": {
                    "hypothesis": (
                        "{format_variant} format will generate {expected_lift}% "
                        "more {metric} than {format_control} for {topic_area} content."
                    ),
                    "typical_duration_days": 30,
                    "minimum_sample_size": 1000,
                    "primary_metrics": ["page_views", "time_on_page", "social_shares"],
                    "guardrail_metrics": ["bounce_rate"],
                },
            },
        ],
        "decision_framework": {
            "implement": {
                "criteria": [
                    "Statistically significant result (p < 0.05)",
                    "Primary metric improved by >= predicted lift",
                    "No guardrail metric breached",
                ],
                "action": "Roll out winning variant to 100% of traffic",
            },
            "iterate": {
                "criteria": [
                    "Directionally positive but not statistically significant",
                    "OR primary metric improved but guardrail breached",
                    "OR insufficient sample size",
                ],
                "action": "Design follow-up experiment with refined hypothesis",
            },
            "discard": {
                "criteria": [
                    "No improvement or negative result",
                    "AND sufficient sample size for conclusion",
                ],
                "action": "Document learning. Do not pursue this direction.",
            },
        },
    }

    output_path = DATA_DIR / "frameworks" / "experiment_frameworks.json"
    with open(output_path, "w") as f:
        json.dump(frameworks, f, indent=2, ensure_ascii=False)

    print(f"  Experiment frameworks: {output_path}")
    return frameworks


def seed_pricing_model():
    """Create engine pricing reference data."""
    pricing = {
        "currency": "USD",
        "market": "Dubai / UAE",
        "last_updated": date.today().isoformat(),
        "engine_pricing": {
            "content_engine": {
                "name": "Content Engine",
                "tiers": {
                    "starter": {
                        "price_monthly": 2500,
                        "includes": [
                            "4 SEO articles/month",
                            "Content calendar",
                            "Basic analytics",
                        ],
                    },
                    "growth": {
                        "price_monthly": 4500,
                        "includes": [
                            "8 SEO articles/month",
                            "Topic cluster strategy",
                            "Content repurposing",
                            "Performance tracking",
                        ],
                    },
                    "scale": {
                        "price_monthly": 7500,
                        "includes": [
                            "12+ articles/month",
                            "Full content strategy",
                            "Multi-format (articles, video scripts, social)",
                            "Dedicated content strategist",
                        ],
                    },
                },
            },
            "seo_engine": {
                "name": "SEO Architecture Engine",
                "tiers": {
                    "starter": {"price_monthly": 2000},
                    "growth": {"price_monthly": 3500},
                    "scale": {"price_monthly": 6000},
                },
            },
            "paid_performance": {
                "name": "Paid Performance Engine",
                "tiers": {
                    "starter": {"price_monthly": 2000, "note": "Plus ad spend"},
                    "growth": {"price_monthly": 3500, "note": "Plus ad spend"},
                    "scale": {"price_monthly": 6000, "note": "Plus ad spend"},
                },
            },
            "social_media": {
                "name": "Social Media Engine",
                "tiers": {
                    "starter": {"price_monthly": 1500},
                    "growth": {"price_monthly": 3000},
                    "scale": {"price_monthly": 5000},
                },
            },
            "email_nurture": {
                "name": "Email Nurture Engine",
                "tiers": {
                    "starter": {"price_monthly": 1500},
                    "growth": {"price_monthly": 2500},
                    "scale": {"price_monthly": 4000},
                },
            },
            "local_visibility": {
                "name": "Local Visibility Engine",
                "tiers": {
                    "starter": {"price_monthly": 1000},
                    "growth": {"price_monthly": 2000},
                    "scale": {"price_monthly": 3500},
                },
            },
            "conversion_optimization": {
                "name": "Conversion Optimization Engine",
                "tiers": {
                    "starter": {"price_monthly": 2000},
                    "growth": {"price_monthly": 3500},
                    "scale": {"price_monthly": 6000},
                },
            },
            "growth_ops": {
                "name": "Growth Ops Engine",
                "tiers": {
                    "growth": {"price_monthly": 5000},
                    "scale": {"price_monthly": 10000},
                },
                "note": "Requires at least 2 other active engines",
            },
        },
        "bundle_discounts": {
            "2_engines": "5% discount",
            "3_engines": "10% discount",
            "4_plus_engines": "15% discount",
            "full_stack": "20% discount (all engines)",
        },
        "audit_pricing": {
            "complimentary_audit": {
                "price": 0,
                "includes": "Full 7-layer growth infrastructure audit",
                "note": "Offered to qualified prospects as lead magnet",
            },
            "premium_audit": {
                "price": 2500,
                "includes": "Audit + strategic roadmap + 60-min strategy session",
                "note": "Credited toward first month if engines engaged",
            },
        },
    }

    output_path = DATA_DIR / "pricing_reference.json"
    with open(output_path, "w") as f:
        json.dump(pricing, f, indent=2, ensure_ascii=False)

    print(f"  Pricing model: {output_path}")
    return pricing


def main():
    """Run all seed functions."""
    print("Apex AI Marketing - Methodology & Benchmark Data Seeder")
    print("=" * 60)
    print()

    ensure_dirs()

    print("Generating methodology showcase data...")
    print()

    seed_methodology_framework()
    seed_industry_benchmarks()
    seed_audit_scoring_rubric()
    seed_experiment_frameworks()
    seed_pricing_model()

    print()
    print("=" * 60)
    print("All methodology data seeded successfully.")
    print(f"Data directory: {DATA_DIR}")
    print()
    print("NOTE: This is methodology documentation and benchmark data,")
    print("NOT fabricated case studies or fake client results.")


if __name__ == "__main__":
    main()

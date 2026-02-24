#!/usr/bin/env python3
"""
Apex AI Marketing - Outreach Template Database Populator

Loads all outreach sequence templates into the database for use by
the outreach automation system.

Creates records for:
  - English email cold sequence (4 steps)
  - Russian email cold sequence (4 steps)
  - LinkedIn DM sequence EN (3 steps)
  - LinkedIn DM sequence RU (3 steps)
  - Telegram community post templates (4 types)
  - Onboarding email templates (3 types x 2 languages)
  - Report delivery templates (2 types x 2 languages)

Usage:
    python scripts/generate_outreach_templates.py

Environment:
    Requires DATABASE_URL to be set or uses default from settings.
"""

import asyncio
import sys
import uuid
from datetime import datetime
from pathlib import Path

# Add parent to path for imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


async def populate_templates():
    """Populate the database with all outreach and email templates."""
    from backend.database import async_session_factory, init_db

    # Ensure tables exist
    await init_db()

    async with async_session_factory() as session:
        from sqlalchemy import text

        # Check if template table exists; create if not
        await session.execute(text("""
            CREATE TABLE IF NOT EXISTS outreach_templates (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                channel VARCHAR(50) NOT NULL,
                language VARCHAR(10) NOT NULL DEFAULT 'en',
                step_number INTEGER NOT NULL DEFAULT 1,
                day_offset INTEGER NOT NULL DEFAULT 0,
                subject TEXT,
                body TEXT NOT NULL,
                placeholders JSONB DEFAULT '[]'::jsonb,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """))
        await session.commit()

        templates_created = 0

        # ── English Email Sequence ────────────────────────────────────
        from backend.templates.emails.outreach_en import OUTREACH_SEQUENCE_EN

        for step, template in OUTREACH_SEQUENCE_EN.items():
            await session.execute(text("""
                INSERT INTO outreach_templates
                    (name, category, channel, language, step_number, day_offset,
                     subject, body, placeholders)
                VALUES
                    (:name, :category, :channel, :language, :step, :day,
                     :subject, :body, :placeholders)
                ON CONFLICT DO NOTHING
            """), {
                "name": template["name"],
                "category": "cold_outreach",
                "channel": "email",
                "language": "en",
                "step": step,
                "day": template["day"],
                "subject": template["subject"],
                "body": template["body"],
                "placeholders": '["name", "company", "specific_finding"]',
            })
            templates_created += 1

        print(f"  English email sequence: {len(OUTREACH_SEQUENCE_EN)} templates")

        # ── Russian Email Sequence ────────────────────────────────────
        from backend.templates.emails.outreach_ru import OUTREACH_SEQUENCE_RU

        for step, template in OUTREACH_SEQUENCE_RU.items():
            await session.execute(text("""
                INSERT INTO outreach_templates
                    (name, category, channel, language, step_number, day_offset,
                     subject, body, placeholders)
                VALUES
                    (:name, :category, :channel, :language, :step, :day,
                     :subject, :body, :placeholders)
                ON CONFLICT DO NOTHING
            """), {
                "name": template["name"],
                "category": "cold_outreach",
                "channel": "email",
                "language": "ru",
                "step": step,
                "day": template["day"],
                "subject": template["subject"],
                "body": template["body"],
                "placeholders": '["name", "company", "specific_finding"]',
            })
            templates_created += 1

        print(f"  Russian email sequence: {len(OUTREACH_SEQUENCE_RU)} templates")

        # ── LinkedIn Sequence EN ──────────────────────────────────────
        from backend.templates.emails.linkedin_sequence import (
            LINKEDIN_SEQUENCE_EN,
            LINKEDIN_SEQUENCE_RU,
        )

        for step, template in LINKEDIN_SEQUENCE_EN.items():
            await session.execute(text("""
                INSERT INTO outreach_templates
                    (name, category, channel, language, step_number, day_offset,
                     subject, body, placeholders)
                VALUES
                    (:name, :category, :channel, :language, :step, :day,
                     '', :body, :placeholders)
                ON CONFLICT DO NOTHING
            """), {
                "name": template["name"],
                "category": "cold_outreach",
                "channel": "linkedin",
                "language": "en",
                "step": step,
                "day": template["day"],
                "body": template["message"],
                "placeholders": '["name", "company", "specific_finding", "industry"]',
            })
            templates_created += 1

        print(f"  LinkedIn EN sequence: {len(LINKEDIN_SEQUENCE_EN)} templates")

        # ── LinkedIn Sequence RU ──────────────────────────────────────
        for step, template in LINKEDIN_SEQUENCE_RU.items():
            await session.execute(text("""
                INSERT INTO outreach_templates
                    (name, category, channel, language, step_number, day_offset,
                     subject, body, placeholders)
                VALUES
                    (:name, :category, :channel, :language, :step, :day,
                     '', :body, :placeholders)
                ON CONFLICT DO NOTHING
            """), {
                "name": template["name"],
                "category": "cold_outreach",
                "channel": "linkedin",
                "language": "ru",
                "step": step,
                "day": template["day"],
                "body": template["message"],
                "placeholders": '["name", "company", "specific_finding", "industry"]',
            })
            templates_created += 1

        print(f"  LinkedIn RU sequence: {len(LINKEDIN_SEQUENCE_RU)} templates")

        # ── Telegram Community Posts ──────────────────────────────────
        from backend.templates.emails.telegram_outreach_ru import (
            TELEGRAM_WEEKLY_INSIGHTS_RU,
        )

        for post_type, template in TELEGRAM_WEEKLY_INSIGHTS_RU.items():
            await session.execute(text("""
                INSERT INTO outreach_templates
                    (name, category, channel, language, step_number, day_offset,
                     subject, body, placeholders)
                VALUES
                    (:name, :category, :channel, :language, 1, 0,
                     '', :body, :placeholders)
                ON CONFLICT DO NOTHING
            """), {
                "name": template["name"],
                "category": "community_content",
                "channel": "telegram",
                "language": "ru",
                "body": template["post"],
                "placeholders": '["topic", "stat", "insight", "cta_link", "week_number"]',
            })
            templates_created += 1

        print(f"  Telegram RU posts: {len(TELEGRAM_WEEKLY_INSIGHTS_RU)} templates")

        # ── Onboarding Templates ──────────────────────────────────────
        from backend.templates.emails.onboarding import ONBOARDING_EN, ONBOARDING_RU

        for lang_code, templates_dict in [("en", ONBOARDING_EN), ("ru", ONBOARDING_RU)]:
            for template_name, template in templates_dict.items():
                await session.execute(text("""
                    INSERT INTO outreach_templates
                        (name, category, channel, language, step_number, day_offset,
                         subject, body, placeholders)
                    VALUES
                        (:name, :category, :channel, :language, 1, 0,
                         :subject, :body, :placeholders)
                    ON CONFLICT DO NOTHING
                """), {
                    "name": f"onboarding_{template_name}",
                    "category": "onboarding",
                    "channel": "email",
                    "language": lang_code,
                    "subject": template["subject"],
                    "body": template["body"],
                    "placeholders": (
                        '["name", "company", "engines", "kickoff_date", '
                        '"kickoff_time", "kickoff_link", "portal_url", "account_manager"]'
                    ),
                })
                templates_created += 1

        print(f"  Onboarding templates: {len(ONBOARDING_EN) + len(ONBOARDING_RU)} templates")

        # ── Report Delivery Templates ─────────────────────────────────
        from backend.templates.emails.report_delivery import (
            REPORT_DELIVERY_EN,
            REPORT_DELIVERY_RU,
        )

        for lang_code, templates_dict in [("en", REPORT_DELIVERY_EN), ("ru", REPORT_DELIVERY_RU)]:
            for report_type, template in templates_dict.items():
                await session.execute(text("""
                    INSERT INTO outreach_templates
                        (name, category, channel, language, step_number, day_offset,
                         subject, body, placeholders)
                    VALUES
                        (:name, :category, :channel, :language, 1, 0,
                         :subject, :body, :placeholders)
                    ON CONFLICT DO NOTHING
                """), {
                    "name": f"report_{report_type}",
                    "category": "report_delivery",
                    "channel": "email",
                    "language": lang_code,
                    "subject": template["subject"],
                    "body": template["body"],
                    "placeholders": (
                        '["name", "company", "period", "highlights", '
                        '"portal_url", "account_manager"]'
                    ),
                })
                templates_created += 1

        print(
            f"  Report delivery templates: "
            f"{len(REPORT_DELIVERY_EN) + len(REPORT_DELIVERY_RU)} templates"
        )

        await session.commit()

        print()
        print(f"Total templates created: {templates_created}")


def main():
    """Entry point."""
    print("Apex AI Marketing - Outreach Template Populator")
    print("=" * 60)
    print()
    print("Loading templates into database...")
    print()

    try:
        asyncio.run(populate_templates())
    except Exception as exc:
        print(f"\nError: {exc}")
        print()
        print("Make sure the database is running and DATABASE_URL is configured.")
        print("You can set it in .env or as an environment variable.")
        sys.exit(1)

    print()
    print("=" * 60)
    print("All outreach templates populated successfully.")


if __name__ == "__main__":
    main()

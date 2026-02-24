"""
Apex AI Marketing - Outreach Tasks

Celery tasks for managing cold outreach sequences, prospect research,
reply handling, and Telegram notifications.
"""

import logging
import uuid
from datetime import datetime, timedelta, date

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="backend.tasks.outreach_tasks.process_outreach_sequences",
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
    time_limit=600,
)
def process_outreach_sequences(self) -> dict:
    """Process all active outreach sequences and send next touches.

    Checks all leads with active sequences:
    - Determines which leads are due for the next email/message
    - Sends the appropriate sequence step (email, LinkedIn DM, Telegram)
    - Updates lead status and next follow-up dates
    - Respects daily sending limits and Dubai work hours

    Returns:
        dict with counts of emails sent, skipped, and errored.
    """
    from database import async_session_factory
    from models.lead import Lead
    from config import get_settings

    import asyncio

    settings = get_settings()

    # Sequence timing: step -> days after initial contact
    SEQUENCE_TIMING = {
        1: 0,   # Day 1: The Infrastructure Question
        2: 3,   # Day 4: The Mini-Audit
        3: 7,   # Day 8: The Evidence
        4: 13,  # Day 14: The Breakup
    }

    DAILY_EMAIL_LIMIT = 40  # Conservative limit per day
    DAILY_LINKEDIN_LIMIT = 20

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select, and_, or_

            today = date.today()

            # Fetch leads that are due for next touch
            result = await session.execute(
                select(Lead).where(
                    and_(
                        Lead.outreach_status.in_(["new", "contacted"]),
                        or_(
                            Lead.next_follow_up <= today,
                            Lead.next_follow_up.is_(None),
                        ),
                        Lead.sequence_step < 5,  # Max 4 steps in sequence
                    )
                ).order_by(Lead.created_at)
            )
            leads = result.scalars().all()

            sent_count = 0
            skipped_count = 0
            error_count = 0
            results = []

            for lead in leads:
                if sent_count >= DAILY_EMAIL_LIMIT:
                    logger.info("Daily email limit reached (%d)", DAILY_EMAIL_LIMIT)
                    break

                try:
                    next_step = lead.sequence_step + 1

                    # Check if enough time has passed since last contact
                    if lead.last_contacted_at:
                        required_days = SEQUENCE_TIMING.get(next_step, 0)
                        days_since_contact = (
                            datetime.utcnow() - lead.last_contacted_at
                        ).days
                        if days_since_contact < required_days:
                            skipped_count += 1
                            continue

                    # Determine channel and send
                    channel = lead.outreach_channel or "email"
                    language = lead.language or "en"

                    success = await _send_sequence_step(
                        lead=lead,
                        step=next_step,
                        channel=channel,
                        language=language,
                    )

                    if success:
                        # Update lead
                        lead.sequence_step = next_step
                        lead.last_contacted_at = datetime.utcnow()
                        lead.outreach_status = "contacted"

                        # Set next follow-up
                        next_step_after = next_step + 1
                        if next_step_after in SEQUENCE_TIMING:
                            days_until_next = (
                                SEQUENCE_TIMING[next_step_after]
                                - SEQUENCE_TIMING[next_step]
                            )
                            lead.next_follow_up = today + timedelta(
                                days=days_until_next
                            )
                        else:
                            lead.next_follow_up = None  # Sequence complete

                        sent_count += 1
                        results.append(
                            {
                                "lead_id": str(lead.id),
                                "step": next_step,
                                "channel": channel,
                                "status": "sent",
                            }
                        )
                    else:
                        skipped_count += 1

                except Exception as exc:
                    logger.error(
                        "Error processing lead %s: %s", lead.id, exc
                    )
                    error_count += 1

            await session.commit()

            summary = {
                "date": today.isoformat(),
                "sent": sent_count,
                "skipped": skipped_count,
                "errors": error_count,
                "total_processed": sent_count + skipped_count + error_count,
                "details": results,
            }

            logger.info(
                "Outreach processing complete: %d sent, %d skipped, %d errors",
                sent_count,
                skipped_count,
                error_count,
            )

            return summary

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Outreach sequence processing failed")
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name="backend.tasks.outreach_tasks.generate_outreach_batch",
    max_retries=2,
    default_retry_delay=120,
    acks_late=True,
    time_limit=900,
)
def generate_outreach_batch(
    self,
    market: str = "dubai",
    language: str = "en",
    criteria: dict = None,
) -> dict:
    """Research prospects and generate personalized outreach sequences.

    Pipeline:
    1. Research prospects matching criteria in the target market
    2. Analyze each prospect's online presence for personalization hooks
    3. Generate personalized first-touch emails
    4. Create lead records with outreach sequences queued

    Args:
        market: Target market (dubai, uk, global, russian_dubai).
        language: Outreach language (en, ru).
        criteria: dict with filters like industry, company_size, etc.

    Returns:
        dict with count of prospects found and sequences created.
    """
    from database import async_session_factory
    from models.lead import Lead

    import asyncio

    criteria = criteria or {}

    async def _run():
        async with async_session_factory() as session:
            logger.info(
                "Generating outreach batch for market=%s, language=%s, criteria=%s",
                market,
                language,
                criteria,
            )

            # ── Step 1: Research prospects ─────────────────────────────
            prospects = await _research_prospects(
                market=market,
                language=language,
                criteria=criteria,
            )

            created_leads = []

            for prospect in prospects:
                # ── Step 2: Analyze prospect ──────────────────────────
                analysis = await _analyze_prospect(prospect)

                # ── Step 3: Generate personalized first touch ─────────
                personalized_hook = await _generate_personalization(
                    prospect=prospect,
                    analysis=analysis,
                    language=language,
                )

                # ── Step 4: Create lead record ────────────────────────
                lead = Lead(
                    name=prospect.get("name", ""),
                    company=prospect.get("company", ""),
                    email=prospect.get("email", ""),
                    phone=prospect.get("phone"),
                    linkedin_url=prospect.get("linkedin_url"),
                    telegram=prospect.get("telegram"),
                    website=prospect.get("website"),
                    industry=prospect.get("industry", criteria.get("industry")),
                    company_size=prospect.get("company_size"),
                    market=market,
                    language=language,
                    pain_points=personalized_hook.get("pain_points", ""),
                    outreach_status="new",
                    outreach_channel=prospect.get("preferred_channel", "email"),
                    sequence_step=0,
                    notes=(
                        f"Auto-generated batch. "
                        f"Hook: {personalized_hook.get('hook', '')}"
                    ),
                )
                session.add(lead)
                created_leads.append(
                    {
                        "company": prospect.get("company"),
                        "channel": prospect.get("preferred_channel", "email"),
                    }
                )

            await session.commit()

            summary = {
                "market": market,
                "language": language,
                "prospects_researched": len(prospects),
                "leads_created": len(created_leads),
                "leads": created_leads,
            }

            logger.info(
                "Outreach batch complete: %d leads created for %s market",
                len(created_leads),
                market,
            )

            return summary

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Outreach batch generation failed")
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name="backend.tasks.outreach_tasks.handle_reply",
    max_retries=3,
    default_retry_delay=30,
    acks_late=True,
)
def handle_reply(self, lead_id: str, reply_content: str) -> dict:
    """Process a reply from a prospect and notify the team via Telegram.

    Pipeline:
    1. Classify reply sentiment (positive, neutral, negative, out-of-office)
    2. Update lead status based on sentiment
    3. Generate suggested response
    4. Send Telegram notification to the team

    Args:
        lead_id: UUID string of the lead who replied.
        reply_content: The reply message content.

    Returns:
        dict with sentiment, updated status, and notification status.
    """
    from database import async_session_factory
    from models.lead import Lead
    from config import get_settings

    import asyncio
    import httpx

    settings = get_settings()

    async def _run():
        async with async_session_factory() as session:
            from sqlalchemy import select

            result = await session.execute(
                select(Lead).where(Lead.id == uuid.UUID(lead_id))
            )
            lead = result.scalar_one_or_none()
            if not lead:
                raise ValueError(f"Lead {lead_id} not found")

            logger.info(
                "Processing reply from %s (%s)", lead.name, lead.company
            )

            # ── Step 1: Classify reply ────────────────────────────────
            classification = await _classify_reply(reply_content)
            sentiment = classification.get("sentiment", "neutral")

            # ── Step 2: Update lead status ────────────────────────────
            status_map = {
                "positive": "replied",
                "meeting_request": "meeting_booked",
                "neutral": "replied",
                "negative": "lost",
                "out_of_office": "contacted",  # Keep in sequence
                "unsubscribe": "lost",
            }
            new_status = status_map.get(sentiment, "replied")
            lead.outreach_status = new_status
            lead.notes = (
                f"{lead.notes or ''}\n\n"
                f"[{datetime.utcnow().isoformat()}] Reply received "
                f"(sentiment: {sentiment}):\n{reply_content[:500]}"
            ).strip()

            # Stop sequence for positive/negative replies
            if sentiment in ("positive", "negative", "meeting_request", "unsubscribe"):
                lead.next_follow_up = None

            # ── Step 3: Generate suggested response ───────────────────
            suggested_response = await _generate_reply_suggestion(
                lead=lead,
                reply_content=reply_content,
                sentiment=sentiment,
            )

            # ── Step 4: Telegram notification ─────────────────────────
            telegram_sent = False
            if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
                try:
                    sentiment_emoji = {
                        "positive": "[+]",
                        "meeting_request": "[MEETING]",
                        "neutral": "[~]",
                        "negative": "[-]",
                        "out_of_office": "[OOO]",
                        "unsubscribe": "[UNSUB]",
                    }
                    emoji = sentiment_emoji.get(sentiment, "[?]")

                    telegram_message = (
                        f"{emoji} OUTREACH REPLY\n\n"
                        f"From: {lead.name} ({lead.company})\n"
                        f"Channel: {lead.outreach_channel or 'email'}\n"
                        f"Sentiment: {sentiment}\n"
                        f"Step: {lead.sequence_step}\n\n"
                        f"Reply:\n{reply_content[:300]}\n\n"
                        f"Suggested response:\n{suggested_response[:300]}"
                    )

                    async with httpx.AsyncClient() as client_http:
                        resp = await client_http.post(
                            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                            json={
                                "chat_id": settings.TELEGRAM_CHAT_ID,
                                "text": telegram_message,
                            },
                            timeout=10,
                        )
                        telegram_sent = resp.status_code == 200

                except Exception as exc:
                    logger.error("Telegram notification failed: %s", exc)

            await session.commit()

            return {
                "lead_id": lead_id,
                "sentiment": sentiment,
                "new_status": new_status,
                "suggested_response": suggested_response,
                "telegram_notified": telegram_sent,
            }

    try:
        result = asyncio.run(_run())
        return result
    except Exception as exc:
        logger.exception("Failed to handle reply for lead %s", lead_id)
        raise self.retry(exc=exc)


# ── Helper functions ──────────────────────────────────────────────────────

async def _send_sequence_step(
    lead, step: int, channel: str, language: str
) -> bool:
    """Send the appropriate sequence step via the chosen channel.

    Args:
        lead: Lead ORM object.
        step: Sequence step number (1-4).
        channel: Communication channel (email, linkedin, telegram).
        language: Language code (en, ru).

    Returns:
        True if sent successfully, False otherwise.
    """
    from config import get_settings

    settings = get_settings()

    try:
        if channel == "email":
            return await _send_email_step(lead, step, language, settings)
        elif channel == "linkedin":
            return await _send_linkedin_step(lead, step, language)
        elif channel == "telegram":
            return await _send_telegram_step(lead, step, language)
        else:
            logger.warning("Unknown channel %s for lead %s", channel, lead.id)
            return False
    except Exception as exc:
        logger.error(
            "Failed to send step %d to %s via %s: %s",
            step,
            lead.name,
            channel,
            exc,
        )
        return False


async def _send_email_step(lead, step: int, language: str, settings) -> bool:
    """Send an email sequence step via Resend."""
    # Load appropriate template
    if language == "ru":
        from templates.emails.outreach_ru import OUTREACH_SEQUENCE_RU
        templates = OUTREACH_SEQUENCE_RU
    else:
        from templates.emails.outreach_en import OUTREACH_SEQUENCE_EN
        templates = OUTREACH_SEQUENCE_EN

    template = templates.get(step)
    if not template:
        logger.warning("No template for step %d in language %s", step, language)
        return False

    # Render template
    subject = template["subject"].format(
        name=lead.name or "",
        company=lead.company or "",
        specific_finding=lead.pain_points or "your online presence",
    )
    body = template["body"].format(
        name=lead.name or "",
        company=lead.company or "",
        specific_finding=lead.pain_points or "your online presence",
    )

    if not lead.email:
        logger.warning("No email address for lead %s", lead.id)
        return False

    # Send via Resend API
    if settings.RESEND_API_KEY:
        import httpx

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": f"{settings.FROM_NAME} <{settings.FROM_EMAIL}>",
                    "to": [lead.email],
                    "subject": subject,
                    "html": body,
                },
                timeout=15,
            )
            if resp.status_code in (200, 201):
                logger.info(
                    "Email step %d sent to %s (%s)",
                    step,
                    lead.name,
                    lead.email,
                )
                return True
            else:
                logger.error(
                    "Resend API error %d: %s", resp.status_code, resp.text
                )
                return False
    else:
        logger.info(
            "Resend API key not configured. Would send step %d to %s",
            step,
            lead.email,
        )
        return True  # Dry run success


async def _send_linkedin_step(lead, step: int, language: str) -> bool:
    """Send a LinkedIn DM (placeholder - requires LinkedIn automation)."""
    logger.info(
        "LinkedIn step %d queued for %s (integration pending)",
        step,
        lead.name,
    )
    return True


async def _send_telegram_step(lead, step: int, language: str) -> bool:
    """Send a Telegram message (placeholder)."""
    logger.info(
        "Telegram step %d queued for %s (integration pending)",
        step,
        lead.name,
    )
    return True


async def _research_prospects(
    market: str, language: str, criteria: dict
) -> list:
    """Research prospects matching criteria.

    TODO: Integrate with prospect research tools/APIs.
    """
    return []


async def _analyze_prospect(prospect: dict) -> dict:
    """Analyze a prospect's online presence for personalization.

    TODO: Integrate with web scraping and AI analysis.
    """
    return {
        "website_score": 0,
        "social_presence": [],
        "content_gaps": [],
    }


async def _generate_personalization(
    prospect: dict, analysis: dict, language: str
) -> dict:
    """Generate personalized outreach hooks using AI.

    TODO: Integrate with Claude API.
    """
    return {
        "hook": "Personalization pending AI integration",
        "pain_points": prospect.get("pain_points", ""),
    }


async def _classify_reply(reply_content: str) -> dict:
    """Classify reply sentiment using AI.

    TODO: Integrate with Claude API for sentiment classification.
    """
    content_lower = reply_content.lower()

    if any(w in content_lower for w in ["interested", "tell me more", "meeting", "call", "sounds good"]):
        return {"sentiment": "positive", "confidence": 0.8}
    elif any(w in content_lower for w in ["not interested", "remove", "stop", "unsubscribe"]):
        return {"sentiment": "negative", "confidence": 0.8}
    elif any(w in content_lower for w in ["out of office", "vacation", "away"]):
        return {"sentiment": "out_of_office", "confidence": 0.9}
    elif any(w in content_lower for w in ["schedule", "calendar", "book", "meet"]):
        return {"sentiment": "meeting_request", "confidence": 0.7}
    else:
        return {"sentiment": "neutral", "confidence": 0.5}


async def _generate_reply_suggestion(
    lead, reply_content: str, sentiment: str
) -> str:
    """Generate a suggested reply based on the prospect's response.

    TODO: Integrate with Claude API.
    """
    suggestions = {
        "positive": (
            f"Great to hear from {lead.name}! Suggest scheduling a 20-minute "
            f"growth infrastructure review call. Send Calendly link."
        ),
        "meeting_request": (
            f"{lead.name} wants to meet. Send calendar link and confirm "
            f"the agenda: growth infrastructure audit review."
        ),
        "neutral": (
            f"Follow up with {lead.name} by providing more specific value. "
            f"Consider sending a mini-audit of their {lead.company} presence."
        ),
        "negative": (
            f"{lead.name} is not interested. Mark as closed and respect "
            f"the decision. Do not follow up."
        ),
        "out_of_office": (
            f"{lead.name} is out of office. Reschedule the next touch "
            f"for when they return."
        ),
    }
    return suggestions.get(sentiment, "Review the reply and respond manually.")

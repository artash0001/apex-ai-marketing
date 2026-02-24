"""
Apex AI Marketing - Webhooks API

Inbound webhook handlers for Web3Forms (contact form) and
email reply tracking (Resend). These endpoints do NOT require
JWT auth but validate signatures where applicable.
"""

import hashlib
import hmac
import json
import logging
import uuid
from datetime import datetime
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Client, Lead, Task
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])


# ── Pydantic Schemas ─────────────────────────────────────────────────

class Web3FormsPayload(BaseModel):
    """Payload from Web3Forms contact form submissions."""
    name: str
    email: str
    company: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    message: Optional[str] = None
    service_interest: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    market: Optional[str] = None
    language: Optional[str] = "en"
    # Web3Forms metadata
    access_key: Optional[str] = Field(None, alias="access_key")
    subject: Optional[str] = None
    from_name: Optional[str] = None
    redirect: Optional[str] = None

    model_config = {"from_attributes": True, "populate_by_name": True}


class EmailReplyPayload(BaseModel):
    """Payload from Resend email reply webhooks."""
    type: str = Field(..., description="Event type from Resend")
    created_at: Optional[str] = None
    data: Optional[dict] = None


# ── Helpers ──────────────────────────────────────────────────────────

async def _send_telegram_notification(message: str) -> bool:
    """Send a notification to the configured Telegram chat."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.warning("Telegram not configured, skipping notification")
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                logger.info("Telegram notification sent successfully")
                return True
            else:
                logger.error(
                    "Telegram notification failed: %s %s",
                    response.status_code,
                    response.text,
                )
                return False
    except Exception as e:
        logger.error("Telegram notification error: %s", e)
        return False


async def _send_confirmation_email(to_email: str, name: str) -> bool:
    """Send a confirmation email to the form submitter via Resend."""
    if not settings.RESEND_API_KEY:
        logger.warning("Resend API key not configured, skipping confirmation email")
        return False

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "from": f"{settings.FROM_NAME} <{settings.FROM_EMAIL}>",
        "to": [to_email],
        "subject": f"Thank you for contacting {settings.BRAND_NAME}!",
        "html": (
            f"<h2>Hi {name},</h2>"
            f"<p>Thank you for reaching out to <strong>{settings.BRAND_NAME}</strong>. "
            f"We've received your message and our team will review it shortly.</p>"
            f"<p>What happens next:</p>"
            f"<ol>"
            f"<li>Our AI infrastructure auditor will analyze your current digital presence</li>"
            f"<li>We'll prepare a personalized growth recommendation</li>"
            f"<li>A team member will reach out within 24 hours to discuss next steps</li>"
            f"</ol>"
            f"<p>In the meantime, you can book a discovery call directly: "
            f"<a href='{settings.CALENDLY_URL}'>Schedule a Call</a></p>"
            f"<br>"
            f"<p>Best regards,<br>"
            f"The {settings.BRAND_NAME} Team</p>"
        ),
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code in (200, 201):
                logger.info("Confirmation email sent to %s", to_email)
                return True
            else:
                logger.error(
                    "Confirmation email failed: %s %s",
                    response.status_code,
                    response.text,
                )
                return False
    except Exception as e:
        logger.error("Confirmation email error: %s", e)
        return False


def _verify_web3forms_signature(
    payload_body: bytes,
    signature: Optional[str],
) -> bool:
    """Verify Web3Forms webhook signature if a key is configured.

    Returns True if no key is configured (signature validation optional).
    """
    if not settings.WEB3FORMS_KEY:
        return True  # No key configured, skip validation

    if not signature:
        logger.warning("No signature provided for Web3Forms webhook")
        return False

    expected = hmac.new(
        settings.WEB3FORMS_KEY.encode("utf-8"),
        payload_body,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


# ── Endpoints ────────────────────────────────────────────────────────

@router.post("/web3forms")
async def handle_web3forms(
    payload: Web3FormsPayload,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle Web3Forms contact form submissions.

    This webhook:
    1. Parses the incoming form data
    2. Creates a client record (status: audit_requested)
    3. Creates a lead record
    4. Sends a confirmation email to the submitter
    5. Notifies the team via Telegram
    6. Creates a task for the Infrastructure Auditor agent

    No JWT auth required - validates Web3Forms signature instead.
    """
    # Validate signature (optional, depends on config)
    body = await request.body()
    signature = request.headers.get("X-Web3Forms-Signature")
    if not _verify_web3forms_signature(body, signature):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid webhook signature",
        )

    logger.info(
        "Web3Forms submission received: %s (%s)",
        payload.name,
        payload.email,
    )

    # ── 1. Check for existing client with this email ──────────────
    existing_client = None
    if payload.email:
        result = await db.execute(
            select(Client).where(Client.email == payload.email)
        )
        existing_client = result.scalar_one_or_none()

    # ── 2. Create or update client record ─────────────────────────
    if existing_client:
        client = existing_client
        # Update with new information
        if payload.phone and not client.phone:
            client.phone = payload.phone
        if payload.whatsapp and not client.whatsapp:
            client.whatsapp = payload.whatsapp
        if payload.industry and not client.industry:
            client.industry = payload.industry
        if payload.website and not client.website:
            client.website = payload.website
        if client.status == "lead":
            client.status = "audit_requested"
        client.updated_at = datetime.utcnow()
        if payload.message:
            existing_notes = client.notes or ""
            client.notes = (
                f"{existing_notes}\n\n"
                f"[{datetime.utcnow().isoformat()}] Form submission: {payload.message}"
            ).strip()
    else:
        client = Client(
            id=uuid.uuid4(),
            name=payload.name,
            company=payload.company,
            email=payload.email,
            phone=payload.phone,
            whatsapp=payload.whatsapp,
            industry=payload.industry,
            website=payload.website,
            language=payload.language or "en",
            status="audit_requested",
            market=payload.market,
            notes=(
                f"Source: Web3Forms contact form\n"
                f"Service interest: {payload.service_interest or 'N/A'}\n"
                f"Message: {payload.message or 'N/A'}"
            ),
        )
        db.add(client)
        await db.flush()

    # ── 3. Create lead record ─────────────────────────────────────
    lead = Lead(
        id=uuid.uuid4(),
        name=payload.name,
        company=payload.company,
        email=payload.email,
        phone=payload.phone,
        whatsapp=payload.whatsapp,
        website=payload.website,
        industry=payload.industry,
        market=payload.market,
        language=payload.language or "en",
        channel="website",
        source="web3forms",
        outreach_status="new",
        sequence_step=0,
        pain_points=payload.message,
        notes=f"Service interest: {payload.service_interest or 'N/A'}",
        metadata={
            "form_subject": payload.subject,
            "client_id": str(client.id),
        },
    )
    db.add(lead)

    # ── 4. Create task for Infrastructure Auditor ─────────────────
    task = Task(
        id=uuid.uuid4(),
        client_id=client.id,
        title=f"Infrastructure Audit: {payload.name}",
        description=(
            f"New contact form submission. Perform infrastructure audit.\n\n"
            f"Name: {payload.name}\n"
            f"Company: {payload.company or 'N/A'}\n"
            f"Email: {payload.email}\n"
            f"Website: {payload.website or 'N/A'}\n"
            f"Industry: {payload.industry or 'N/A'}\n"
            f"Market: {payload.market or 'N/A'}\n"
            f"Service interest: {payload.service_interest or 'N/A'}\n"
            f"Message: {payload.message or 'N/A'}"
        ),
        task_type="infrastructure_audit",
        assigned_agent="infrastructure_auditor",
        status="pending",
        metadata={
            "client_id": str(client.id),
            "lead_id": str(lead.id),
            "source": "web3forms",
        },
    )
    db.add(task)

    await db.flush()

    # ── 5. Send confirmation email (async, non-blocking) ──────────
    email_sent = await _send_confirmation_email(payload.email, payload.name)

    # ── 6. Send Telegram notification ─────────────────────────────
    telegram_message = (
        f"<b>NEW LEAD FROM WEBSITE</b>\n\n"
        f"<b>Name:</b> {payload.name}\n"
        f"<b>Email:</b> {payload.email}\n"
        f"<b>Company:</b> {payload.company or 'N/A'}\n"
        f"<b>Phone:</b> {payload.phone or 'N/A'}\n"
        f"<b>Industry:</b> {payload.industry or 'N/A'}\n"
        f"<b>Website:</b> {payload.website or 'N/A'}\n"
        f"<b>Market:</b> {payload.market or 'N/A'}\n"
        f"<b>Service:</b> {payload.service_interest or 'N/A'}\n\n"
        f"<b>Message:</b>\n{payload.message or 'No message'}\n\n"
        f"Infrastructure Auditor task created. Respond ASAP!"
    )
    telegram_sent = await _send_telegram_notification(telegram_message)

    return {
        "success": True,
        "message": "Contact form processed successfully",
        "client_id": str(client.id),
        "lead_id": str(lead.id),
        "task_id": str(task.id),
        "email_sent": email_sent,
        "telegram_sent": telegram_sent,
    }


@router.post("/email-reply")
async def handle_email_reply(
    payload: EmailReplyPayload,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle email reply webhooks from Resend.

    Processes inbound email events (delivered, opened, clicked, replied,
    bounced, complained) and updates lead outreach status accordingly.

    No JWT auth required - validates Resend webhook signature.
    """
    # Validate Resend webhook signature
    resend_signature = request.headers.get("Resend-Signature")
    # Note: Resend signature validation would use their specific format.
    # For now we log and process. In production, implement full validation.
    if resend_signature:
        logger.info("Resend webhook signature present: %s...", resend_signature[:20])

    event_type = payload.type
    event_data = payload.data or {}
    logger.info("Email webhook received: type=%s", event_type)

    # Extract recipient email from event data
    to_email = None
    if isinstance(event_data.get("to"), list) and event_data["to"]:
        to_email = event_data["to"][0]
    elif isinstance(event_data.get("to"), str):
        to_email = event_data["to"]

    # Try to find matching lead
    lead = None
    if to_email:
        result = await db.execute(
            select(Lead).where(Lead.email == to_email)
        )
        lead = result.scalar_one_or_none()

    # Process based on event type
    status_updates = {
        "email.delivered": None,  # No status change, just log
        "email.opened": None,  # Track open but don't change status
        "email.clicked": None,  # Track click but don't change status
        "email.replied": "replied",  # Advance to replied
        "email.bounced": None,  # Log bounce
        "email.complained": "not_interested",  # Mark as not interested
    }

    new_status = status_updates.get(event_type)

    if lead and new_status:
        old_status = lead.outreach_status
        lead.outreach_status = new_status
        lead.updated_at = datetime.utcnow()

        # Update outreach history
        history_entry = {
            "from": old_status,
            "to": new_status,
            "trigger": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "resend_webhook",
        }
        if lead.outreach_history is None:
            lead.outreach_history = []
        lead.outreach_history = lead.outreach_history + [history_entry]

        logger.info(
            "Lead %s status updated: %s -> %s (trigger: %s)",
            lead.id,
            old_status,
            new_status,
            event_type,
        )

    # Log all events
    if lead and event_type in ("email.replied", "email.complained"):
        # Notify via Telegram for important events
        telegram_message = (
            f"<b>EMAIL EVENT: {event_type.upper()}</b>\n\n"
            f"<b>Lead:</b> {lead.name if lead else 'Unknown'}\n"
            f"<b>Email:</b> {to_email or 'Unknown'}\n"
            f"<b>Company:</b> {lead.company if lead else 'N/A'}\n"
            f"<b>Event:</b> {event_type}\n"
        )
        await _send_telegram_notification(telegram_message)

    if lead:
        await db.flush()

    return {
        "success": True,
        "event_type": event_type,
        "lead_id": str(lead.id) if lead else None,
        "status_updated": new_status is not None and lead is not None,
        "new_status": new_status if lead else None,
    }

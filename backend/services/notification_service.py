"""
Apex AI Marketing - Telegram Notification Service

Sends formatted notifications to the founder's Telegram chat
via the Bot API. Used for alerts, status updates, and daily summaries.
"""

import logging

import httpx

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

TELEGRAM_API_BASE = "https://api.telegram.org"


class NotificationService:
    """Sends Telegram messages to the configured chat."""

    def __init__(self) -> None:
        self._token = settings.TELEGRAM_BOT_TOKEN
        self._chat_id = settings.TELEGRAM_CHAT_ID

    @property
    def _send_url(self) -> str:
        return f"{TELEGRAM_API_BASE}/bot{self._token}/sendMessage"

    # ── Core send method ──────────────────────────────────────────────
    async def send_notification(self, message: str) -> bool:
        """Send a Telegram message. Returns True on success.

        The message is sent with HTML parse mode so you can use
        ``<b>bold</b>``, ``<i>italic</i>``, and ``<code>mono</code>``.
        """
        if not self._token or not self._chat_id:
            logger.warning("Telegram not configured - skipping notification")
            return False

        payload = {
            "chat_id": self._chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(self._send_url, json=payload)
                resp.raise_for_status()
                logger.info("Telegram notification sent successfully")
                return True
        except httpx.HTTPStatusError as exc:
            logger.error(
                "Telegram API error %d: %s",
                exc.response.status_code,
                exc.response.text,
            )
            return False
        except httpx.RequestError as exc:
            logger.error("Telegram request error: %s", exc)
            return False

    # ── Convenience helpers ───────────────────────────────────────────

    async def notify_new_lead(self, name: str, company: str, industry: str) -> bool:
        """Notify about a new audit request from the website."""
        msg = (
            "\U0001F514 <b>New audit request</b>\n\n"
            f"<b>Name:</b> {name}\n"
            f"<b>Company:</b> {company}\n"
            f"<b>Industry:</b> {industry}\n\n"
            "Check the admin panel for details."
        )
        return await self.send_notification(msg)

    async def notify_deliverables_ready(self, count: int) -> bool:
        """Daily digest: deliverables awaiting review."""
        msg = (
            f"\U0001F4E6 <b>{count} deliverable(s)</b> ready for review today.\n\n"
            "Open the admin panel to review and approve."
        )
        return await self.send_notification(msg)

    async def notify_new_client(
        self, company: str, engines: list[str]
    ) -> bool:
        """Notify that a new client has been activated."""
        engine_list = ", ".join(engines) if engines else "TBD"
        msg = (
            "\U0001F680 <b>New active client</b>\n\n"
            f"<b>Company:</b> {company}\n"
            f"<b>Engines:</b> {engine_list}\n\n"
            "Onboarding sequence initiated."
        )
        return await self.send_notification(msg)

    async def notify_error(self, context: str, error: str) -> bool:
        """Alert about a system error."""
        msg = (
            "\U0001F6A8 <b>System Error</b>\n\n"
            f"<b>Context:</b> {context}\n"
            f"<b>Error:</b> <code>{error}</code>"
        )
        return await self.send_notification(msg)

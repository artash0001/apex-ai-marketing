"""
Apex AI Marketing - Email Service

Sends transactional emails via the Resend API.
Supports plain HTML and Jinja2 template rendering.
"""

import logging
from pathlib import Path

import resend
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# ── Jinja2 template environment ──────────────────────────────────────
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "emails"

_jinja_env: Environment | None = None


def _get_jinja_env() -> Environment:
    global _jinja_env
    if _jinja_env is None:
        if TEMPLATES_DIR.exists():
            _jinja_env = Environment(
                loader=FileSystemLoader(str(TEMPLATES_DIR)),
                autoescape=select_autoescape(["html", "xml"]),
            )
        else:
            # Fallback: create the directory so it exists for future use
            TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
            _jinja_env = Environment(
                loader=FileSystemLoader(str(TEMPLATES_DIR)),
                autoescape=select_autoescape(["html", "xml"]),
            )
    return _jinja_env


class EmailService:
    """Sends transactional emails through the Resend API."""

    def __init__(self) -> None:
        resend.api_key = settings.RESEND_API_KEY

    # ── Send raw HTML email ───────────────────────────────────────────
    async def send_email(
        self,
        to: str | list[str],
        subject: str,
        html_body: str,
        from_email: str | None = None,
    ) -> dict | None:
        """Send an email with an HTML body.

        Parameters
        ----------
        to : str or list[str]
            Recipient email address(es).
        subject : str
            Email subject line.
        html_body : str
            Full HTML content.
        from_email : str, optional
            Override the default sender.

        Returns
        -------
        dict or None
            Resend API response on success, None on failure.
        """
        sender = from_email or f"{settings.FROM_NAME} <{settings.FROM_EMAIL}>"
        if isinstance(to, str):
            to = [to]

        try:
            params: resend.Emails.SendParams = {
                "from": sender,
                "to": to,
                "subject": subject,
                "html": html_body,
            }
            response = resend.Emails.send(params)
            logger.info("Email sent to %s: subject=%s", to, subject)
            return response
        except Exception as exc:
            logger.error("Failed to send email to %s: %s", to, exc)
            return None

    # ── Send templated email ──────────────────────────────────────────
    async def send_template_email(
        self,
        to: str | list[str],
        subject: str,
        template_name: str,
        context: dict | None = None,
        from_email: str | None = None,
    ) -> dict | None:
        """Render a Jinja2 template and send it.

        Parameters
        ----------
        to : str or list[str]
            Recipient email address(es).
        subject : str
            Email subject line.
        template_name : str
            Filename inside ``templates/emails/``, e.g. ``"welcome.html"``.
        context : dict, optional
            Variables available inside the template.
        from_email : str, optional
            Override the default sender.
        """
        ctx = context or {}
        # Always make brand info available in templates
        ctx.setdefault("brand_name", settings.BRAND_NAME)
        ctx.setdefault("site_url", settings.SITE_URL)
        ctx.setdefault("calendly_url", settings.CALENDLY_URL)

        env = _get_jinja_env()
        try:
            template = env.get_template(template_name)
        except Exception as exc:
            logger.error("Template %s not found: %s", template_name, exc)
            return None

        html_body = template.render(**ctx)
        return await self.send_email(
            to=to,
            subject=subject,
            html_body=html_body,
            from_email=from_email,
        )

"""Production email provider — sends emails via Resend API.

Purpose:
    Renders email templates and sends them through Resend's transactional
    email service. Used in production when email_provider="resend".

Does NOT do:
    - Template rendering (each template has its own renderer)
    - Rate limiting (Resend handles that)

Who depends on this:
    AuthService calls EmailService.send() during signup and
    forgot-password flows.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from typing import TYPE_CHECKING

import resend

if TYPE_CHECKING:
    from app.modules.platform.notifications.email_service import EmailMessage

from app.modules.platform.notifications.emails.reset_password import render_reset_password
from app.modules.platform.notifications.emails.verify_email import render_verify_email

logger = logging.getLogger("app.modules.platform.notifications.resend")

_TEMPLATE_MAP: dict[str, Callable[..., tuple[str, str]]] = {
    "verify-email": render_verify_email,
    "reset-password": render_reset_password,
}


class ResendEmailProvider:
    def __init__(self, api_key: str, from_address: str) -> None:
        self._from_address = from_address
        resend.api_key = api_key

    async def send(self, message: EmailMessage) -> None:
        renderer = _TEMPLATE_MAP.get(message.template)
        if not renderer:
            raise ValueError(f"Unknown email template: {message.template}")

        subject, html = renderer(**message.context)

        emails = resend.Emails()
        params: resend.Emails.SendParams = {
            "from": self._from_address,
            "to": [message.to],
            "subject": subject,
            "html": html,
        }
        await asyncio.to_thread(emails.send, params)

        logger.info(
            "Email sent type=%s recipient=%s provider=resend",
            message.template,
            message.to,
        )

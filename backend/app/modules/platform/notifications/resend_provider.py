from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.platform.notifications.email_service import EmailMessage

from app.modules.platform.notifications.emails.reset_password import render_reset_password
from app.modules.platform.notifications.emails.verify_email import render_verify_email

_TEMPLATE_MAP = {
    "verify_email": render_verify_email,
    "reset_password": render_reset_password,
}


class ResendEmailProvider:
    def __init__(self, api_key: str, from_address: str) -> None:
        self._api_key = api_key
        self._from_address = from_address

    async def send(self, message: EmailMessage) -> None:
        renderer = _TEMPLATE_MAP.get(message.template)
        if not renderer:
            raise ValueError(f"Unknown email template: {message.template}")

        subject, html = renderer(**message.context)

        try:
            from resend import Emails
        except ImportError:
            raise ImportError("pip install resend is required for ResendEmailProvider")

        emails = Emails(api_key=self._api_key)
        await emails.send(
            from_address=self._from_address,
            to=[message.to],
            subject=subject,
            html=html,
        )

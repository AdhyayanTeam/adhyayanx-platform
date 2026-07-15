"""Development email provider — logs emails to console instead of sending.

Purpose:
    Allows local development and testing without an email service.
    Emails are printed to the console in a readable format.

Does NOT actually send emails — use ResendEmailProvider in production.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.platform.notifications.email_service import EmailMessage

logger = logging.getLogger("app.modules.platform.notifications.console")


class ConsoleEmailProvider:
    async def send(self, message: EmailMessage) -> None:
        lines = [
            "",
            "=" * 60,
            f"  TO:      {message.to}",
            f"  SUBJECT: {message.subject}",
            f"  TEMPLATE: {message.template}",
            "-" * 60,
        ]
        for key, value in message.context.items():
            lines.append(f"  {key}: {value}")
        lines.append("=" * 60)
        lines.append("")
        logger.info("\n".join(lines))

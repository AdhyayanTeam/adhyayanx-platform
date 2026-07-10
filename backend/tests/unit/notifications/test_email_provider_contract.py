"""Contract test: EmailService protocol implementations."""

from __future__ import annotations

from app.modules.platform.notifications.console_provider import ConsoleEmailProvider
from app.modules.platform.notifications.email_service import EmailMessage


class TestEmailProviderContract:

    async def test_console_provider_sends_without_error(self) -> None:
        provider = ConsoleEmailProvider()

        message = EmailMessage(
            template="test-template",
            to="test@example.com",
            subject="Test Subject",
            context={"name": "Test", "url": "https://example.com"},
        )

        await provider.send(message)

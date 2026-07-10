from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.platform.notifications.email_service import EmailMessage


class ResendEmailProvider:
    def __init__(self, api_key: str, from_address: str) -> None:
        self._api_key = api_key
        self._from_address = from_address

    async def send(self, message: EmailMessage) -> None:
        raise NotImplementedError("ResendEmailProvider: not yet wired")

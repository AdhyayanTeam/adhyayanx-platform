from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class EmailMessage:
    template: str
    to: str
    subject: str
    context: dict[str, str] = field(default_factory=dict)


class EmailService(Protocol):
    async def send(self, message: EmailMessage) -> None: ...

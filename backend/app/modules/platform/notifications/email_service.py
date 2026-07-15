"""Email service interface and message model.

Purpose:
    Defines the structural contract for sending emails. Implementations
    (ConsoleEmailProvider, ResendEmailProvider) satisfy this protocol.

Does NOT do:
    - Template rendering (each template module handles that)
    - Choose the provider (Settings and main.py wire the right one)

Who depends on this:
    AuthService calls EmailService.send() for verification and
    password reset emails.
"""

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

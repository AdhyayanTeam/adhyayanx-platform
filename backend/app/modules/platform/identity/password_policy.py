from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.foundation.exceptions.base import ValidationError

if TYPE_CHECKING:
    from app.kernel.config.loader import Settings

logger = logging.getLogger("app.modules.platform.identity.password_policy")

_COMMON_PASSWORDS: set[str] = {
    "password",
    "password123",
    "12345678",
    "qwerty123",
    "admin123",
    "welcome123",
    "letmein",
    "monkey123",
    "dragon123",
    "master123",
    "shadow123",
    "sunshine",
    "trustno1",
    "iloveyou",
    "batman123",
    "football",
}

_hasher = PasswordHasher()


class PasswordPolicy:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def validate(self, password: str, context: str | None = None) -> None:
        errors: list[str] = []

        if len(password) < self._settings.password_min_length:
            errors.append(
                f"Password must be at least {self._settings.password_min_length} characters"
            )
        if len(password) > self._settings.password_max_length:
            errors.append(
                f"Password must be at most {self._settings.password_max_length} characters"
            )

        if self._settings.password_require_upper and not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")

        if self._settings.password_require_lower and not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")

        if self._settings.password_require_digit and not re.search(r"\d", password):
            errors.append("Password must contain at least one digit")

        if self._settings.password_require_special and not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]", password
        ):
            errors.append("Password must contain at least one special character")

        if password.lower() in _COMMON_PASSWORDS:
            errors.append("This password is too common. Choose a different one.")

        if context and context.lower() in password.lower():
            errors.append("Password must not contain your email or name")

        if errors:
            raise ValidationError("; ".join(errors))

    @staticmethod
    def hash_password(password: str) -> str:
        return _hasher.hash(password)

    @staticmethod
    def verify_password(password_hash: str, password: str) -> bool:
        try:
            return _hasher.verify(password_hash, password)
        except VerifyMismatchError:
            return False

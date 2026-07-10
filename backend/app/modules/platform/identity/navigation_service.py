from __future__ import annotations

import logging

logger = logging.getLogger("app.modules.platform.identity.navigation_service")

_SOLUTION_DOMAINS: dict[str, str] = {
    "clinic": "clinic.adhyayanx.in",
    "academy": "academy.adhyayanx.in",
    "gym": "gym.adhyayanx.in",
    "salon": "salon.adhyayanx.in",
}

_DEFAULT_LANDING = "console.adhyayanx.in"


class NavigationService:
    @staticmethod
    def resolve_landing(blueprint_codes: list[str]) -> str:
        for code in blueprint_codes:
            domain = _SOLUTION_DOMAINS.get(code)
            if domain:
                return domain
        return _DEFAULT_LANDING

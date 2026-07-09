from __future__ import annotations

import importlib
import pkgutil
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from kernel.container import Container


def discover_blueprints(container: Container) -> list[str]:
    """Discover blueprint packages by scanning the blueprints directory."""
    import blueprints

    discovered: list[str] = []
    for _, name, is_pkg in pkgutil.iter_modules(blueprints.__path__):
        if is_pkg:
            module = importlib.import_module(f"blueprints.{name}")
            if hasattr(module, "register"):
                module.register(container)
                discovered.append(name)
    return discovered


def discover_handlers(container: Container) -> dict[str, list[Any]]:
    """Discover event handlers across all registered modules."""
    handlers: dict[str, list[Any]] = {}
    handler_modules = [
        "adx_platform.events.handlers",
        "adx_platform.organizations.handlers",
        "adx_platform.identity.handlers",
    ]
    for module_path in handler_modules:
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, "register_handlers"):
                module.register_handlers(handlers)
        except ImportError:
            continue
    return handlers

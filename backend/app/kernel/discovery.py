from __future__ import annotations

import importlib
import pkgutil
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.kernel.container import Container


def discover_blueprints(container: Container) -> list[str]:
    """Discover blueprint packages by scanning the blueprints directory."""
    import app.modules.blueprints as blueprints

    discovered: list[str] = []
    for _, name, is_pkg in pkgutil.iter_modules(blueprints.__path__):
        if is_pkg:
            module = importlib.import_module(f"app.modules.blueprints.{name}")
            if hasattr(module, "register"):
                module.register(container)
                discovered.append(name)
    return discovered


def discover_handlers(container: Container) -> dict[str, list[Any]]:
    """Discover event handlers registered by extension blueprints."""
    handlers: dict[str, list[Any]] = {}
    try:
        import app.modules.blueprints as blueprints
    except ImportError:
        return handlers
    for _, name, is_pkg in pkgutil.iter_modules(blueprints.__path__):
        if is_pkg:
            try:
                module = importlib.import_module(f"app.modules.blueprints.{name}")
                if hasattr(module, "register_handlers"):
                    module.register_handlers(handlers)
            except ImportError:
                continue
    return handlers

from __future__ import annotations

from typing import Any, TypeVar

T = TypeVar("T")


class Container:
    """Simple DI container. Registry maps interfaces to implementations."""

    def __init__(self) -> None:
        self._registry: dict[type, type] = {}
        self._instances: dict[type, Any] = {}

    def register(self, interface: type[T], implementation: type[T]) -> None:
        self._registry[interface] = implementation

    def register_instance(self, interface: type[T], instance: T) -> None:
        self._instances[interface] = instance

    def resolve(self, interface: type[T]) -> T:
        if interface in self._instances:
            return self._instances[interface]  # type: ignore[no-any-return]
        implementation = self._registry.get(interface)
        if implementation is None:
            name = getattr(interface, "__name__", str(interface))
            raise KeyError(f"No implementation registered for {name}")
        instance = self._build(implementation)
        self._instances[interface] = instance
        return instance  # type: ignore[no-any-return]

    def _build(self, implementation: type) -> Any:
        from inspect import signature

        params = signature(implementation.__init__).parameters  # type: ignore[misc]
        kwargs = {}
        for name, param in params.items():
            if name == "self":
                continue
            annotation = param.annotation
            if annotation is not param.empty:
                resolved = self._resolve_annotation(annotation)
                if resolved is not None:
                    try:
                        kwargs[name] = self.resolve(resolved)
                    except KeyError:
                        if param.default is not param.empty:
                            continue
                        name_label = getattr(resolved, "__name__", str(resolved))
                        raise KeyError(
                            f"Cannot resolve dependency '{name}: {name_label}' "
                            f"for {implementation.__name__}"
                        ) from None
        return implementation(**kwargs)

    def _resolve_annotation(self, annotation: Any) -> Any | None:
        if not isinstance(annotation, str):
            return annotation
        for t in list(self._registry) + list(self._instances):
            if t.__name__ == annotation:
                return t
        if annotation == "Settings":
            from app.kernel.config.loader import Settings
            return Settings
        import re
        for part in re.split(r"\s*\|\s*", annotation):
            part = part.strip()
            if part == "None":
                continue
            for t in list(self._registry) + list(self._instances):
                if hasattr(t, "__name__") and t.__name__ == part:
                    return t
        return None

    def clear(self) -> None:
        self._registry.clear()
        self._instances.clear()

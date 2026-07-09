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
            return self._instances[interface]
        implementation = self._registry.get(interface)
        if implementation is None:
            raise KeyError(f"No implementation registered for {interface.__name__}")
        instance = self._build(implementation)
        self._instances[interface] = instance
        return instance

    def _build(self, implementation: type) -> Any:
        from inspect import signature
        params = signature(implementation.__init__).parameters
        kwargs = {}
        for name, param in params.items():
            if name == "self":
                continue
            if param.annotation is not param.empty:
                try:
                    kwargs[name] = self.resolve(param.annotation)
                except KeyError as e:
                    raise KeyError(
                        f"Cannot resolve dependency '{name}: {param.annotation.__name__}' "
                        f"for {implementation.__name__}"
                    ) from e
        return implementation(**kwargs)

    def clear(self) -> None:
        self._registry.clear()
        self._instances.clear()

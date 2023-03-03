from abc import ABC, abstractproperty
from logging import getLogger
from typing import Generic, Protocol, Type, TypeVar


class DomainEvent(ABC):
    name = ""

    @abstractproperty
    def id(self) -> str:
        raise NotImplementedError


T = TypeVar("T", bound=DomainEvent)


class EventListener(Generic[T]):
    def listen(self, event: T) -> None:
        raise NotImplementedError


class EventBus(Protocol):
    def publish(self, *events: DomainEvent) -> None:
        raise NotImplementedError


class InMemoryEventBus:

    event_mapping: dict[str, list[EventListener]] = {}
    logger = getLogger("InMemoryEventBus")

    def register(
        self, event: Type[DomainEvent], listeners: list[EventListener]
    ) -> None:
        self.event_mapping[event.name] = listeners

    def _publish(self, event: DomainEvent) -> None:
        listeners = self.event_mapping.get(event.name)
        if not listeners:
            self.logger.warn(f"No event listeners for {event.name}")
            return
        for listener in listeners:
            listener.listen(event)

    def publish(self, *events: DomainEvent) -> None:
        for event in events:
            self.logger.info(f"Publishing event: {event.name}")
            self._publish(event)

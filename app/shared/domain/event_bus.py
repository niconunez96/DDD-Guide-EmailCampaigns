from abc import ABC, abstractproperty
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


class DomainEvent(ABC):
    id: UUID

    @abstractproperty
    def name(self) -> str:
        raise NotImplementedError


class EventListener:
    def listen(self, event: DomainEvent) -> None:
        raise NotImplementedError


class EventBus(Protocol):
    def publish(self, event: DomainEvent) -> None:
        raise NotImplementedError


class InMemoryEventBus:

    event_mapping: dict[str, list[EventListener]] = {}

    def register(self, event: DomainEvent, listeners: list[EventListener]) -> None:
        self.event_mapping[event.name] = listeners

    def publish(self, event: DomainEvent) -> None:
        listeners = self.event_mapping.get(event.name)
        if not listeners:
            return
        for listener in listeners:
            listener.listen(event)

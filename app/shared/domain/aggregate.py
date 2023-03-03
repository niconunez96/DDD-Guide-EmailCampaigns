import abc
from typing import Generic, Optional, Type, TypeVar
from uuid import UUID, uuid4

T = TypeVar("T", bound="DomainId")


class DomainId(abc.ABC, Generic[T]):
    value: UUID

    def __str__(self) -> str:
        return str(self.value)

    def __init__(self, value: Optional[UUID] = None) -> None:
        self.value = value or uuid4()

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, DomainId) and self.value == __o.value

    def __hash__(self) -> int:
        return hash(self.value)

    @classmethod
    def from_string(cls: Type[T], value: str) -> Optional[T]:
        try:
            id = UUID(value)
            return cls(id)
        except Exception:
            return None

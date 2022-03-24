import abc
from typing import Generic, Optional, Type, TypeVar
from uuid import UUID, uuid4


T = TypeVar("T", bound="DomainId")


class DomainId(abc.ABC, Generic[T]):
    value: UUID

    def __str__(self) -> str:
        return str(self.value)

    def __init__(self, value: UUID = None) -> None:
        self.value = value or uuid4()

    @classmethod
    def from_string(cls: Type[T], value: str) -> Optional[T]:
        try:
            id = UUID(value)
            return cls(id)
        except:
            return None

from __future__ import annotations

import abc
from typing import Generic, Optional, Type, TypeVar
from uuid import UUID


T = TypeVar("T", bound="DomainId")


class DomainId(abc.ABC, Generic[T]):
    def __str__(self) -> str:
        return str(self.value)

    def __init__(self, value: UUID) -> None:
        pass

    @classmethod
    def from_string(cls: Type[T], value: str) -> Optional[T]:
        try:
            id = UUID(value)
            return cls(id)
        except:
            return None

    @abc.abstractproperty
    def value(self) -> UUID:
        raise NotImplementedError

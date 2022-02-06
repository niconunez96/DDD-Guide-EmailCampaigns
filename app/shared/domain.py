from __future__ import annotations

import abc
from uuid import UUID


class DomainId(abc.ABC):
    def __str__(self) -> str:
        return str(self.value)

    def __init__(self, value: UUID) -> None:
        pass

    @staticmethod
    @abc.abstractstaticmethod
    def from_string(value: str) -> DomainId:
        raise NotImplementedError

    @abc.abstractproperty
    def value(self) -> UUID:
        raise NotImplementedError

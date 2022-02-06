from __future__ import annotations

import abc
from uuid import UUID


class DomainId(abc.ABC):
    value: UUID

    def __str__(self) -> str:
        return str(self.value)

    @abc.abstractstaticmethod
    def from_string(value) -> DomainId:
        raise NotImplementedError

from dataclasses import dataclass
from uuid import UUID
from app.shared.domain import DomainId


@dataclass(frozen=True)
class ContactListId(DomainId):
    _id: UUID

    def value(self) -> UUID:
        return self._id


class ContactList:
    _id: ContactListId
    _contacts: list[str]

    def __init__(self, id: ContactListId, contacts: list[str]):
        self._id = id
        self._contacts = contacts

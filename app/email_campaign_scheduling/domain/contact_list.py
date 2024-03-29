from functools import total_ordering
from typing import Literal, Optional, TypedDict

from app.shared.domain.aggregate import DomainId

ContactStatus = Literal["BOUNCED", "DELIVERABLE"]


class ContactResponse(TypedDict):
    id: int
    email: str
    status: str


class Contact:
    id: int
    _user_id: str
    _email: str
    _status: ContactStatus

    def __init__(self, user_id: str, email: str, status: ContactStatus = "DELIVERABLE"):
        self._email = email
        self._status = status
        self._user_id = user_id

    @property
    def to_response(self) -> ContactResponse:
        return {
            "id": self.id,
            "email": self._email,
            "status": self._status,
        }


@total_ordering
class ContactListId(DomainId["ContactListId"]):
    def __lt__(self, other: "ContactListId") -> bool:
        return str(self.value) < str(other.value)


class ContactList:
    id: ContactListId
    _user_id: str
    _name: str
    _contacts: list[Contact]
    _contacts_quantity: int

    def __init__(
        self, id: ContactListId, user_id: str, name: str, contacts: Optional[list[Contact]] = None
    ):
        self.id = id
        self._user_id = user_id
        self._name = name
        self._contacts = contacts or []
        self._contacts_quantity = len(self._contacts)

    @property
    def contacts(self) -> list[ContactResponse]:
        return [contact.to_response for contact in self._contacts]

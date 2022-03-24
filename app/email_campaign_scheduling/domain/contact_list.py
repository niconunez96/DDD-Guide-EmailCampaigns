from typing import Literal, TypedDict
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


class ContactListId(DomainId["ContactListId"]):
    pass


class ContactList:
    id: ContactListId
    _user_id: str
    _name: str
    _contacts: list[Contact]

    def __init__(
        self, id: ContactListId, user_id: str, name: str, contacts: list[Contact] = None
    ):
        self.id = id
        self._user_id = user_id
        self._name = name
        self._contacts = contacts or []

    @property
    def contacts(self) -> list[ContactResponse]:
        return [contact.to_response for contact in self._contacts]

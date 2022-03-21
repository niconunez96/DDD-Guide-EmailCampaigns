from dataclasses import dataclass
from typing import Literal
from uuid import UUID
from app.shared.domain import DomainId


ContactStatus = Literal["BOUNCED", "DELIVERABLE"]


class Contact:
    id: int
    _user_id: str
    _email: str
    _status: ContactStatus

    def __init__(self, user_id: str, email: str, status: ContactStatus = "DELIVERABLE"):
        self._email = email
        self._status = status
        self._user_id = user_id


class ContactListId(DomainId["ContactListId"]):
    pass


class ContactList:
    id: ContactListId
    _user_id: str
    _name: str
    _contacts: list[Contact]

    def __init__(
        self, id: ContactListId, user_id: str, name: str, contacts: list[Contact]
    ):
        self.id = id
        self._user_id = user_id
        self._name = name
        self._contacts = contacts or []

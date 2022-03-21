from typing import Optional, Protocol, Type
from .contact_list import ContactList, ContactListId
from app.shared.infra.db import MySQLRepo, SessionFactory
from sqlalchemy.orm import scoped_session


class ContactListRepo(Protocol):
    def store(self, contact_list: ContactList) -> None:
        raise NotImplementedError

    def find_by_id(self, id: str) -> Optional[ContactList]:
        raise NotImplementedError


class ContactListMySQLRepo(MySQLRepo[ContactList, ContactListId]):
    def store(self, contact_list: ContactList) -> None:
        super().save(contact_list)

    def find_by_id(self, id: ContactListId) -> Optional[ContactList]:
        return super().find_by_id(id)

    @property
    def _clz(self) -> Type[ContactList]:
        return ContactList

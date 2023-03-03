from typing import Optional, Protocol, Type

from sqlalchemy.orm import joinedload, scoped_session

from app.shared.infra.db import MySQLRepo, SessionFactory

from .contact_list import ContactList, ContactListId


class ContactListRepo(Protocol):
    def store(self, contact_list: ContactList) -> None:
        raise NotImplementedError

    def find_by_id(
        self, id: ContactListId, with_contacts: bool = False
    ) -> Optional[ContactList]:
        raise NotImplementedError

    def find(self, ids: list[ContactListId]) -> list[ContactList]:
        raise NotImplementedError


class ContactListMySQLRepo(MySQLRepo[ContactList, ContactListId]):
    def store(self, contact_list: ContactList) -> None:
        super()._save(contact_list)

    def find_by_id(
        self, id: ContactListId, with_contacts: bool = False
    ) -> Optional[ContactList]:
        if with_contacts:
            session = scoped_session(SessionFactory)
            contact_list: Optional[ContactList] = (
                session.query(ContactList)
                .options(joinedload("_contacts"))
                .filter_by(id=id)
                .first()
            )
            session.close()
            return contact_list
        return super()._find_by_id(id)

    def find(self, ids: list[ContactListId]) -> list[ContactList]:
        session = scoped_session(SessionFactory)
        contact_lists = (
            session.query(ContactList).filter(ContactList.id.in_(ids)).all()  # type: ignore
        )
        session.close()
        return contact_lists

    @property
    def _clz(self) -> Type[ContactList]:
        return ContactList


contact_list_mysql_repo = ContactListMySQLRepo()

from dataclasses import dataclass
from typing import Optional
from app.scheduling.domain.contact_list import ContactList, ContactListId
from app.scheduling.domain.contact_list_repo import (
    ContactListRepo,
    contact_list_mysql_repo,
)


@dataclass(frozen=True)
class CreateContactListCommand:
    id: ContactListId
    name: str
    user_id: str


def create_contact_list(
    cmd: CreateContactListCommand,
    contact_list_repo: ContactListRepo = contact_list_mysql_repo,
) -> None:
    contact_list = ContactList(
        id=cmd.id,
        name=cmd.name,
        user_id=cmd.user_id,
    )
    contact_list_repo.store(contact_list)

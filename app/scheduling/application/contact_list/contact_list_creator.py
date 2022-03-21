from dataclasses import dataclass, field
from app.scheduling.domain.contact_list import Contact, ContactList, ContactListId
from app.scheduling.domain.contact_list_repo import (
    ContactListRepo,
    contact_list_mysql_repo,
)


@dataclass(frozen=True)
class CreateContactListCommand:
    id: ContactListId
    name: str
    user_id: str
    contacts: list[str] = field(default_factory=lambda: [])


def create_contact_list(
    cmd: CreateContactListCommand,
    contact_list_repo: ContactListRepo = contact_list_mysql_repo,
) -> None:
    contacts = [Contact(cmd.user_id, email=contact) for contact in cmd.contacts]
    contact_list = ContactList(
        id=cmd.id,
        name=cmd.name,
        user_id=cmd.user_id,
        contacts=contacts,
    )
    contact_list_repo.store(contact_list)

from app.email_campaign_scheduling.domain.contact_list import ContactListId, ContactResponse
from app.email_campaign_scheduling.domain.contact_list_repo import (
    ContactListRepo,
    contact_list_mysql_repo,
)


def find_contacts(
    contact_list_id: ContactListId,
    contact_list_repo: ContactListRepo = contact_list_mysql_repo,
) -> list[ContactResponse]:
    contact_list = contact_list_repo.find_by_id(contact_list_id, with_contacts=True)
    if not contact_list:
        raise Exception("Contact list not found")
    return contact_list.contacts

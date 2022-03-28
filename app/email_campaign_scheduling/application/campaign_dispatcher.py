from logging import getLogger
from typing import Optional, cast
from app.email_campaign_scheduling.application.contact_list import find_contacts
from app.email_campaign_scheduling.application.sender.sender_finder import find_sender
from app.email_campaign_scheduling.domain.campaign import CampaignId
from app.email_campaign_scheduling.domain.campaign_repo import (
    CampaignRepo,
    campaign_mysql_repo,
)
from app.email_campaign_scheduling.domain.contact_list import ContactListId
from app.email_campaign_scheduling.domain.contact_list_repo import (
    contact_list_mysql_repo,
    ContactListRepo,
)
from app.email_campaign_scheduling.domain.sender import SenderId, SenderResponse
from app.email_campaign_scheduling.infra.email_sender import (
    EmailSender,
    sendgrid_email_sender,
)

logger = getLogger(__name__)


def _find_sender(sender_id: str) -> Optional[SenderResponse]:
    id = SenderId.from_string(sender_id)
    if not id:
        logger.warning(f"Sender id is invalid")
        return None
    sender = find_sender(id)
    return sender


def dispatch_campaign(
    id: CampaignId,
    campaign_repo: CampaignRepo = campaign_mysql_repo,
    contact_list_repo: ContactListRepo = contact_list_mysql_repo,
    email_sender: EmailSender = sendgrid_email_sender,
) -> None:
    campaign = campaign_repo.find(id)
    if not campaign:
        logger.warning(f"Campaign with id {id} not found")
        return
    sender = _find_sender(campaign._user_id)
    if not sender:
        logger.warning(f"There is no sender with id {campaign._user_id}")
        return
    contact_list_ids = [
        cast(ContactListId, ContactListId.from_string(target.contact_list_id))
        for target in campaign._contact_list_targets
    ]
    contact_lists = contact_list_repo.find(contact_list_ids)
    contact_lists_to_send = campaign.calculate_contact_lists_to_send(
        sender["daily_send_limit"], contact_lists
    )
    if not contact_lists_to_send:
        campaign.mark_as_sent()
    else:
        for contact_list_to_send in contact_lists_to_send:
            contacts = find_contacts(contact_list_to_send.contact_list_id)[
                0 : contact_list_to_send.quantity_limit
            ]
            campaign_response = campaign.to_response()
            email_sender.send_emails(
                {
                    "subject": campaign_response["subject"],
                    "body": campaign_response["body"],
                    "sender_email": campaign_response["sender"],
                    "sender_id": sender["id"],
                    "campaign_id": campaign_response["id"],
                    "recipient_emails": (contact["email"] for contact in contacts),
                }
            )
        campaign.schedule_for_tomorrow(contact_lists_sent=dict(contact_lists_to_send))
    campaign_repo.update(campaign)

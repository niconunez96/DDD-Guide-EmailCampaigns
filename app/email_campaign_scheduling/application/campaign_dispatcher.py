from logging import getLogger
from app.email_campaign_scheduling.application.contact_list import find_contacts
from app.email_campaign_scheduling.application.sender.sender_finder import find_sender
from app.email_campaign_scheduling.application.sender.sender_current_limit_updater import (
    update_sender_current_limit,
)
from app.email_campaign_scheduling.domain.campaign import (
    Campaign,
    CampaignId,
    ContactListsToSend,
)
from app.email_campaign_scheduling.domain.campaign_repo import (
    CampaignRepo,
    campaign_mysql_repo,
)
from app.email_campaign_scheduling.domain.contact_list_repo import (
    contact_list_mysql_repo,
    ContactListRepo,
)
from app.email_campaign_scheduling.domain.sender import SenderId, SenderResponse
from app.email_campaign_scheduling.domain.sender_repo import (
    SenderRepo,
    sender_mysql_repo,
)
from app.email_campaign_scheduling.infra.email_sender import (
    EmailSender,
    sendgrid_email_sender,
)

logger = getLogger(__name__)


def _find_campaign(id: CampaignId, campaign_repo: CampaignRepo) -> Campaign:
    campaign = campaign_repo.find(id)
    if not campaign:
        logger.warning(f"Campaign with id {id} not found")
        raise Exception("CAMPAIGN_NOT_FOUND")
    return campaign


def _find_sender(id: SenderId, sender_repo: SenderRepo) -> SenderResponse:
    sender = find_sender(id, sender_repo)
    if not sender:
        logger.warning(f"There is no sender with id {id}")
        raise Exception("SENDER_NOT_FOUND")
    return sender


def _grab_contact_lists_to_send(
    campaign: Campaign,
    sender_info: SenderResponse,
    contact_list_repo: ContactListRepo,
) -> ContactListsToSend:
    contact_list_ids = [
        target.contact_list_id for target in campaign._contact_list_targets
    ]
    contact_lists = contact_list_repo.find(contact_list_ids)
    contact_lists_to_send = campaign.calculate_contact_lists_to_send(
        sender_info["current_limit"], contact_lists
    )

    return contact_lists_to_send


def _send_campaign(
    email_sender: EmailSender,
    campaign: Campaign,
    sender_info: SenderResponse,
    contact_lists_to_send: ContactListsToSend,
) -> None:
    if contact_lists_to_send.should_reschedule_campaign:
        campaign.schedule_for_tomorrow(dict(contact_lists_to_send.contact_lists))
    if not contact_lists_to_send.should_reschedule_campaign:
        campaign.mark_as_sent()
    for contact_list_to_send in contact_lists_to_send.contact_lists:
        contacts = find_contacts(contact_list_to_send.contact_list_id)[
            0 : contact_list_to_send.quantity_limit
        ]
        campaign_response = campaign.to_response()
        email_sender.send_emails(
            {
                "subject": campaign_response["subject"],
                "body": campaign_response["body"],
                "sender_email": campaign_response["sender"],
                "sender_id": sender_info["id"],
                "campaign_id": campaign_response["id"],
                "recipient_emails": (contact["email"] for contact in contacts),
            }
        )


def dispatch_campaign(
    id: CampaignId,
    campaign_repo: CampaignRepo = campaign_mysql_repo,
    sender_repo: SenderRepo = sender_mysql_repo,
    contact_list_repo: ContactListRepo = contact_list_mysql_repo,
    email_sender: EmailSender = sendgrid_email_sender,
) -> None:
    campaign = _find_campaign(id, campaign_repo)
    sender_info = _find_sender(campaign._sender_id, sender_repo)
    contact_lists_to_send = _grab_contact_lists_to_send(
        campaign, sender_info, contact_list_repo
    )
    update_sender_current_limit(
        campaign._sender_id,
        total_used=sum(
            contact_list_to_send.quantity_limit
            for contact_list_to_send in contact_lists_to_send.contact_lists
        ),
        sender_repo=sender_repo,
    )
    _send_campaign(email_sender, campaign, sender_info, contact_lists_to_send)
    campaign_repo.update(campaign)

from dataclasses import dataclass

from app.email_campaign_scheduling.domain.campaign import CampaignId
from app.email_campaign_scheduling.domain.campaign_repo import (
    CampaignRepo,
    campaign_mysql_repo,
)
from app.email_campaign_scheduling.domain.contact_list import ContactListId
from app.email_campaign_scheduling.domain.contact_list_repo import (
    ContactListRepo,
    contact_list_mysql_repo,
)


@dataclass(frozen=True)
class AddCampaignToContactListCommand:
    campaign_id: CampaignId
    contact_list_ids: list[ContactListId]


def add_contact_lists(
    cmd: AddCampaignToContactListCommand,
    campaign_repo: CampaignRepo = campaign_mysql_repo,
    contact_list_repo: ContactListRepo = contact_list_mysql_repo,
) -> None:
    campaign = campaign_repo.find(cmd.campaign_id)
    if not campaign:
        raise Exception("CAMPAIGN_NOT_FOUND")
    contact_lists = contact_list_repo.find(cmd.contact_list_ids)
    if not contact_lists:
        raise Exception("CONTACT_LISTS_NOT_FOUND")
    campaign.add_contact_lists(contact_lists)
    campaign_repo.update(campaign)

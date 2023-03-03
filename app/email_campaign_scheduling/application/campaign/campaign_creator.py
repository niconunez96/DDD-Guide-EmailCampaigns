from dataclasses import dataclass
from logging import getLogger
from uuid import UUID

from app.email_campaign_scheduling.domain.campaign import Campaign, CampaignId
from app.email_campaign_scheduling.domain.campaign_repo import (
    CampaignRepo,
    campaign_mysql_repo,
)
from app.email_campaign_scheduling.domain.sender import SenderId

logger = getLogger(__name__)


@dataclass(frozen=True)
class CreateCampaignCommand:
    id: UUID
    name: str
    subject: str
    body: str
    sender_email: str
    sender_id: str


def create_campaign(
    command: CreateCampaignCommand,
    campaign_repo: CampaignRepo = campaign_mysql_repo,
) -> None:
    sender_id = SenderId.from_string(command.sender_id)
    if not sender_id:
        raise Exception("INVALID_SENDER_ID")
    campaign = Campaign(
        CampaignId(command.id),
        command.name,
        command.subject,
        command.body,
        command.sender_email,
        sender_id,
    )
    logger.info(campaign)
    campaign_repo.store(campaign)

from typing import Optional
from uuid import UUID
from dataclasses import dataclass
from logging import getLogger

from app.email_campaign_scheduling.domain.campaign import Campaign, CampaignId
from app.email_campaign_scheduling.domain.campaign_repo import (
    CampaignRepo,
    campaign_mysql_repo,
)

logger = getLogger(__name__)


@dataclass(frozen=True)
class CreateCampaignCommand:
    id: UUID
    name: str
    subject: str
    body: str
    sender: str
    user_id: str


def create_campaign(
    command: CreateCampaignCommand,
    campaign_repo: CampaignRepo = campaign_mysql_repo,
) -> None:
    campaign = Campaign(
        CampaignId(command.id),
        command.name,
        command.subject,
        command.body,
        command.sender,
        command.user_id,
    )
    logger.info(campaign)
    campaign_repo.store(campaign)

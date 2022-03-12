from typing import Optional
from uuid import UUID
from dataclasses import dataclass
from logging import getLogger

from ..domain.campaign import Campaign, CampaignId
from ..domain.campaign_repo import CampaignRepo, campaign_mysql_repo

logger = getLogger(__name__)


@dataclass(frozen=True)
class CreateCampaignCommand:
    id: UUID
    name: str
    subject: str
    body: str
    sender: str


def create_campaign(
    command: CreateCampaignCommand,
    campaign_repo: Optional[CampaignRepo] = None,
) -> None:
    campaign_repo = campaign_repo or campaign_mysql_repo
    campaign = Campaign(
        CampaignId(command.id),
        command.name,
        command.subject,
        command.body,
        command.sender,
    )
    logger.info(campaign)
    campaign_repo.store(campaign)
    return

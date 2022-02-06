from dataclasses import dataclass
from logging import getLogger

from ..domain.campaign import Campaign

logger = getLogger(__name__)


@dataclass(frozen=True)
class CreateCampaignCommand:
    name: str
    subject: str
    body: str
    sender: str


def create_campaign(command: CreateCampaignCommand) -> None:
    campaign = Campaign(command.name, command.subject, command.body, command.sender)
    logger.info(campaign)
    return

from dataclasses import dataclass
from datetime import datetime
from app.scheduling.domain.campaign import CampaignId
from app.scheduling.domain.campaign_repo import CampaignRepo


@dataclass(frozen=True)
class ScheduleCommand:
    id: CampaignId
    schedule_datetime: datetime


def schedule_campaign(campaign_repo: CampaignRepo, cmd: ScheduleCommand) -> None:
    campaign = campaign_repo.find(cmd.id)
    if not campaign:
        raise Exception("Campaign does not exist")
    campaign._schedule_datetime = cmd.schedule_datetime
    campaign_repo.update(campaign)

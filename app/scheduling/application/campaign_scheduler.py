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


# Alternative
# This is an example alternative which is CRUD oriented
# We don't choose this alternative because it's very generic and does not represent the
# real intention of the use case, we only want to modify the schedule time explictly
# in a particular use case

@dataclass(frozen=True)
class UpdateInfo:
    id: CampaignId
    schedule_datetime: datetime
    name: str

def update_campaign(campaign_repo: CampaignRepo, info: UpdateInfo) -> None:
    campaign = campaign_repo.find(info.id)
    if not campaign:
        raise Exception("Campaign does not exist")
    campaign._schedule_datetime = info.schedule_datetime or campaign._schedule_datetime
    campaign._name = info.name or campaign._name
    campaign_repo.update(campaign)

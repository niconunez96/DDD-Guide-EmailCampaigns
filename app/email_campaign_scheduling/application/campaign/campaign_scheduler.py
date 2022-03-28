from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.email_campaign_scheduling.domain.campaign import CampaignId
from app.email_campaign_scheduling.domain.campaign_repo import CampaignRepo, campaign_mysql_repo


@dataclass(frozen=True)
class ScheduleCommand:
    id: CampaignId
    schedule_datetime: datetime


def schedule_campaign(
    cmd: ScheduleCommand, campaign_repo: Optional[CampaignRepo] = None
) -> None:
    campaign_repo = campaign_repo or campaign_mysql_repo
    campaign = campaign_repo.find(cmd.id)
    if not campaign:
        raise Exception("Campaign does not exist")
    campaign.schedule(cmd.schedule_datetime)
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


def update_campaign(
    info: UpdateInfo, campaign_repo: Optional[CampaignRepo] = None
) -> None:
    campaign_repo = campaign_repo or campaign_mysql_repo
    campaign = campaign_repo.find(info.id)
    if not campaign:
        raise Exception("Campaign does not exist")
    campaign._name = info.name or campaign._name
    if info.schedule_datetime:
        campaign.schedule(info.schedule_datetime)
    campaign_repo.update(campaign)

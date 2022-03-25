from typing import Optional

from app.email_campaign_scheduling.domain.campaign import CampaignId, CampaignResponse
from app.email_campaign_scheduling.domain.campaign_repo import (
    CampaignRepo,
    campaign_mysql_repo,
)


def find_campaign(
    id: CampaignId, campaign_repo: CampaignRepo = campaign_mysql_repo
) -> Optional[CampaignResponse]:
    campaign = campaign_repo.find(id)
    if not campaign:
        return None
    return campaign.to_response()


def find_user_campaigns(
    user_id: str, campaign_repo: CampaignRepo = campaign_mysql_repo
) -> list[CampaignResponse]:
    campaigns = campaign_repo.find_by_user(user_id)
    return [campaign.to_response() for campaign in campaigns]

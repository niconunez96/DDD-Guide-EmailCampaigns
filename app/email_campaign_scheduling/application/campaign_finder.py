from typing import Optional

from ..domain.campaign import CampaignId, CampaignResponse
from ..domain.campaign_repo import CampaignRepo, campaign_mysql_repo


def find_campaign(
    id: CampaignId, campaign_repo: Optional[CampaignRepo] = None
) -> Optional[CampaignResponse]:
    campaign_repo = campaign_repo or campaign_mysql_repo
    campaign = campaign_repo.find(id)
    if not campaign:
        return None
    return campaign.to_response()

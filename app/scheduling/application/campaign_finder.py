from typing import Optional

from ..domain.campaign import CampaignId, CampaignResponse
from ..domain.campaign_repo import CampaignRepo


def find_campaign(
    campaign_repo: CampaignRepo, id: CampaignId
) -> Optional[CampaignResponse]:
    campaign = campaign_repo.find(id)
    if not campaign:
        return None
    return campaign.to_response()

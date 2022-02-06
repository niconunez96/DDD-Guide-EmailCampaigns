from typing import Optional
from ..domain.campaign import Campaign, CampaignId
from ..domain.campaign_repo import CampaignRepo


def find_campaign(campaign_repo: CampaignRepo, id: CampaignId) -> Optional[Campaign]:
    return campaign_repo.find(id)

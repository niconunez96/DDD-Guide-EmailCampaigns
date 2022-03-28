from app.email_campaign_scheduling.domain.campaign import CampaignId
from app.email_campaign_scheduling.domain.campaign_repo import (
    CampaignRepo,
    campaign_mysql_repo,
)
from app.email_campaign_scheduling.application.campaign_dispatcher import (
    dispatch_campaign,
)


def send_now(id: CampaignId, campaign_repo: CampaignRepo = campaign_mysql_repo) -> None:
    campaign = campaign_repo.find(id)
    if not campaign:
        raise Exception("CAMPAIGN_NOT_FOUND")
    campaign.start_sending()
    campaign_repo.update(campaign)
    dispatch_campaign(id)

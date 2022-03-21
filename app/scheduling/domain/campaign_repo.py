from typing import Optional, Protocol, Type

from app.shared.infra.db import MySQLRepo

from .campaign import Campaign, CampaignId


class CampaignRepo(Protocol):
    def store(self, campaign: Campaign) -> None:
        raise NotImplementedError

    def find(self, id: CampaignId) -> Optional[Campaign]:
        raise NotImplementedError

    def update(self, campaign: Campaign) -> None:
        raise NotImplementedError


class CampaignMySQLRepo(MySQLRepo[Campaign, CampaignId]):
    def store(self, campaign: Campaign) -> None:
        super()._save(campaign)

    def find(self, id: CampaignId) -> Optional[Campaign]:
        return super()._find_by_id(id)

    def update(self, campaign: Campaign) -> None:
        super()._save(campaign)

    def _clz(self) -> Type[Campaign]:
        return Campaign


campaign_mysql_repo = CampaignMySQLRepo()

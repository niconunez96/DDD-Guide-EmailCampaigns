from typing import Optional, Protocol, Type, overload

from app.shared.infra.db import MySQLRepo, SessionFactory
from sqlalchemy.orm import scoped_session
from .campaign import Campaign, CampaignId


class CampaignRepo(Protocol):
    def store(self, campaign: Campaign) -> None:
        raise NotImplementedError

    def find(self, id: CampaignId) -> Optional[Campaign]:
        raise NotImplementedError

    def find_by_user(self, user_id: str) -> list[Campaign]:
        raise NotImplementedError

    def update(self, campaign: Campaign) -> None:
        raise NotImplementedError


class CampaignMySQLRepo(MySQLRepo[Campaign, CampaignId]):
    def store(self, campaign: Campaign) -> None:
        super()._save(campaign)

    def find(self, id: CampaignId) -> Optional[Campaign]:
        return super()._find_by_id(id)

    def find_by_user(self, user_id: str) -> list[Campaign]:
        session = scoped_session(SessionFactory)
        campaigns: list[Campaign] = session.query(Campaign).filter_by(_user_id=user_id).all()
        session.close()
        return campaigns

    def update(self, campaign: Campaign) -> None:
        super()._save(campaign)

    @property
    def _clz(self) -> Type[Campaign]:
        return Campaign


campaign_mysql_repo = CampaignMySQLRepo()

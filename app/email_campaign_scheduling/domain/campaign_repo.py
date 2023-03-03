from typing import Optional, Protocol, Type

from sqlalchemy.orm import raiseload, scoped_session

from app.shared.infra.db import MySQLRepo, SessionFactory

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
        campaigns: list[Campaign] = (
            session.query(Campaign)
            .options(raiseload("_contact_list_targets"))
            .filter_by(_user_id=user_id)
            .all()
        )
        session.close()
        return campaigns

    def update(self, campaign: Campaign) -> None:
        super()._save(campaign)

    @property
    def _clz(self) -> Type[Campaign]:
        return Campaign


campaign_mysql_repo = CampaignMySQLRepo()

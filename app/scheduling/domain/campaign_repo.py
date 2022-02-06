from typing import Optional, Protocol

from app.db import SessionFactory
from sqlalchemy.orm import scoped_session

from .campaign import Campaign, CampaignId


class CampaignRepo(Protocol):
    def store(self, campaign: Campaign) -> None:
        raise NotImplementedError

    def find(self, id: CampaignId) -> Optional[Campaign]:
        raise NotImplementedError


class CampaignMySQLRepo:
    def store(self, campaign: Campaign) -> None:
        session = scoped_session(SessionFactory)
        session.add(campaign)
        session.commit()
        session.close()

    def find(self, id: CampaignId) -> Optional[Campaign]:
        session = scoped_session(SessionFactory)
        campaign: Optional[Campaign] = session.query(Campaign).filter_by(id=id).first()
        session.close()
        return campaign


campaign_mysql_repo = CampaignMySQLRepo()

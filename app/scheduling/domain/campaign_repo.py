from typing import Protocol

from app.db import SessionFactory
from sqlalchemy.orm import scoped_session

from .campaign import Campaign


class CampaignRepo(Protocol):
    def store(self, campaign: Campaign) -> None:
        raise NotImplementedError


class CampaignMySQLRepo:
    def store(self, campaign: Campaign) -> None:
        session = scoped_session(SessionFactory)
        session.add(campaign)
        session.commit()

campaign_mysql_repo = CampaignMySQLRepo()

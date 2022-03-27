from abc import ABC, abstractproperty
from typing import Generic, Optional, Type, TypeVar
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.email_campaign_scheduling.infra.campaign_db import create_campaign_schema
from app.email_campaign_scheduling.infra.contact_list_db import (
    create_contact_list_schema,
)
from app.email_campaign_scheduling.infra.user_db import (
    create_user_table as create_campaign_user_table,
)
from app.marketing.infra.user_db import create_user_table


engine = create_engine("mysql+mysqldb://root:39853201@localhost:3306/email_campaign", echo=True)
metadata = MetaData()
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    create_campaign_schema(metadata)
    create_contact_list_schema(metadata)
    create_user_table(metadata)
    create_campaign_user_table(metadata)
    metadata.create_all(bind=engine)


T = TypeVar("T")
ID = TypeVar("ID")


class MySQLRepo(Generic[T, ID], ABC):
    def _save(self, entity: T) -> None:
        session = scoped_session(SessionFactory)
        session.add(entity)
        session.commit()
        session.close()

    def _find_by_id(self, id: ID) -> Optional[T]:
        session = scoped_session(SessionFactory)
        entity = session.query(self._clz).filter_by(id=id).first()
        session.close()
        return entity

    @abstractproperty
    def _clz(self) -> Type[T]:
        raise NotImplementedError

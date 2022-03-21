from abc import ABC, abstractproperty
from typing import Generic, Optional, Type, TypeVar
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.scheduling.infra.campaign_db import create_campaign_schema
from app.scheduling.infra.contact_list_db import create_contact_list_schema
from app.shared.domain import DomainId

engine = create_engine("mysql+mysqldb://root:39853201@localhost:3306/email_campaign")
metadata = MetaData()
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    create_campaign_schema(metadata)
    create_contact_list_schema(metadata)
    metadata.create_all(bind=engine)


T = TypeVar("T")
ID = TypeVar("ID")

class MySQLRepo(Generic[T, ID], ABC):
    def save(self, entity: T) -> None:
        session = scoped_session(SessionFactory)
        session.add(entity)
        session.commit()
        session.close()

    def find_by_id(self, id: ID) -> Optional[T]:
        session = scoped_session(SessionFactory)
        entity: Optional[T] = session.query(self._clz).filter_by(id=id).first()
        session.close()
        return entity

    @abstractproperty
    def _clz(self) -> Type[T]:
        raise NotImplementedError

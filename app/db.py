import uuid

from sqlalchemy import Column, MetaData, String, Table, create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy_utils import UUIDType

from .model import Campaign

engine = create_engine("sqlite:////tmp/test.db")
metadata = MetaData()
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

campaign_table = Table(
    "campaigns",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True, default=uuid.uuid4),
    Column("name", String(50)),
    Column("subject", String(50)),
)
mapper(Campaign, campaign_table)


def init_db():
    metadata.create_all(bind=engine)

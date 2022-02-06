from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from app.scheduling.infra.campaign_db import create_campaign_schema

engine = create_engine("sqlite:////tmp/test.db")
metadata = MetaData()
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    create_campaign_schema(metadata)
    metadata.create_all(bind=engine)

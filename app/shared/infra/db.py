from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from app.scheduling.infra.campaign_db import create_campaign_schema
from app.scheduling.infra.contact_list_db import create_contact_list_schema

engine = create_engine("mysql+mysqldb://root:39853201@localhost:3306/email_campaign")
metadata = MetaData()
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    create_campaign_schema(metadata)
    create_contact_list_schema(metadata)
    metadata.create_all(bind=engine)

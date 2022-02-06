import uuid

from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.orm import mapper
from sqlalchemy_utils import UUIDType

from ..domain.campaign import Campaign


def create_campaign_schema(metadata: MetaData) -> None:
    campaign_table = Table(
        "campaigns",
        metadata,
        Column("id", UUIDType(binary=False), primary_key=True, default=uuid.uuid4),
        Column("name", String(50), key="_name"),
        Column("subject", String(50), key="_subject"),
        Column("body", String(50), key="_body"),
        Column("sender", String(50), key="_sender"),
    )
    mapper(Campaign, campaign_table)

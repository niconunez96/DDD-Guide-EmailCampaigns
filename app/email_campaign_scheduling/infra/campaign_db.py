from app.shared.infra.sqlalchemy_types import DomainIdObjectType
from sqlalchemy import Column, MetaData, String, Table, DateTime, ForeignKey
from sqlalchemy.orm import registry
from sqlalchemy_utils import UUIDType

from ..domain.campaign import Campaign, CampaignId


mapper_registry = registry()


def create_campaign_schema(metadata: MetaData) -> None:
    campaign_table = Table(
        "campaigns",
        metadata,
        Column(
            "id",
            DomainIdObjectType(CampaignId, UUIDType(binary=False)),
            primary_key=True,
        ),
        Column("name", String(50), key="_name"),
        Column("subject", String(50), key="_subject"),
        Column("body", String(50), key="_body"),
        Column("sender", String(50), key="_sender"),
        Column("schedule_datetime", DateTime(), key="_schedule_datetime"),
        Column("status", String(10), key="_status"),
        Column("user_id", String(50), key="_user_id"),
    )
    mapper_registry.map_imperatively(Campaign, campaign_table)

from app.shared.infra.sqlalchemy_types import DomainIdObjectType
from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.orm import mapper
from sqlalchemy_utils import UUIDType

from ..domain.campaign import Campaign, CampaignId


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
    )
    mapper(Campaign, campaign_table)

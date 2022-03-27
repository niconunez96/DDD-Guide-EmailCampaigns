from app.shared.infra.sqlalchemy_types import DomainIdObjectType
from sqlalchemy import Column, MetaData, String, Table, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import registry
from sqlalchemy_utils import UUIDType

from ..domain.campaign import Campaign, CampaignId, ContactListTarget


mapper_registry = registry()


def create_campaign_schema(metadata: MetaData) -> None:
    contact_list_target_table = Table(
        "contact_list_targets",
        metadata,
        Column(
            "id",
            Integer(),
            primary_key=True,
            autoincrement=True,
        ),
        Column("contact_list_id", String(50)),
        Column(
            "campaign_id",
            DomainIdObjectType(CampaignId, UUIDType(binary=False)),
            ForeignKey("campaigns.id"),
        ),
    )
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
    mapper_registry.map_imperatively(ContactListTarget, contact_list_target_table)
    mapper_registry.map_imperatively(
        Campaign,
        campaign_table,
        properties={
            "_contact_list_targets": relationship(
                "ContactListTarget",
                lazy="joined",
                collection_class=set,
            )
        },
    )

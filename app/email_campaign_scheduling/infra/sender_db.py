from app.shared.infra.sqlalchemy_types import DomainIdObjectType
from sqlalchemy import Column, MetaData, Table, Integer, Date
from sqlalchemy.orm.decl_api import registry
from sqlalchemy_utils import UUIDType

from ..domain.sender import Sender, SenderId


mapper_registry = registry()


def create_user_table(metadata: MetaData) -> None:
    user_table = Table(
        "senders",
        metadata,
        Column(
            "id",
            DomainIdObjectType(SenderId, UUIDType(binary=False)),
            primary_key=True,
        ),
        Column("daily_send_limit", Integer(), key="daily_send_limit"),
        Column("current_limit", Integer(), key="_current_limit"),
        Column(
            "current_limit_updated_at",
            Date(),
            key="_last_time_current_limit_was_updated",
        ),
    )
    mapper_registry.map_imperatively(Sender, user_table)

from app.shared.infra.sqlalchemy_types import DomainIdObjectType
from sqlalchemy import Column, MetaData, Table, Integer
from sqlalchemy.orm import registry
from sqlalchemy_utils import UUIDType

from ..domain.user import User, UserId


mapper_registry = registry()


def create_user_table(metadata: MetaData) -> None:
    user_table = Table(
        "users",
        metadata,
        Column(
            "id",
            DomainIdObjectType(UserId, UUIDType(binary=False)),
            primary_key=True,
        ),
        Column("plan", Integer(), key="_plan"),
    )
    mapper_registry.map_imperatively(User, user_table)

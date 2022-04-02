from app.shared.infra.sqlalchemy_types import DomainIdObjectType
from sqlalchemy import Column, MetaData, Table, Enum
from sqlalchemy.orm.decl_api import registry
from sqlalchemy_utils import UUIDType

from ..domain.user import MarketingPlan, User, UserId


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
        Column("plan", Enum(MarketingPlan), key="_plan"),
    )
    mapper_registry.map_imperatively(User, user_table)

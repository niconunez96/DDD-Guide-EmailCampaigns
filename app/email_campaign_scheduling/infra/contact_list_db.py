from app.shared.infra.sqlalchemy_types import DomainIdObjectType
from sqlalchemy import Column, MetaData, String, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import registry
from sqlalchemy_utils import UUIDType

from ..domain.contact_list import Contact, ContactList, ContactListId


mapper_registry = registry()


def create_contact_list_schema(metadata: MetaData) -> None:
    contact_table = Table(
        "contacts",
        metadata,
        Column(
            "id",
            Integer(),
            primary_key=True,
            autoincrement=True,
        ),
        Column("user_id", String(50), key="_user_id"),
        Column("email", String(50), key="_email"),
        Column("status", String(20), key="_status"),
    )
    contact_list_table = Table(
        "contact_lists",
        metadata,
        Column(
            "id",
            DomainIdObjectType(ContactListId, UUIDType(binary=False)),
            primary_key=True,
        ),
        Column("user_id", String(50), key="_user_id"),
        Column("name", String(50), key="_name"),
        Column("status", String(20), key="_status"),
    )

    contact_list_X_contacts_table = Table(
        "contact_lists_X_contacts",
        metadata,
        Column(
            "contact_list_id",
            DomainIdObjectType(ContactListId, UUIDType(binary=False)),
            ForeignKey("contact_lists.id"),
        ),
        Column("contact_id", Integer(), ForeignKey("contacts.id")),
    )

    mapper_registry.map_imperatively(Contact, contact_table)
    mapper_registry.map_imperatively(
        ContactList,
        contact_list_table,
        properties={
            "_contacts": relationship(
                "Contact", secondary=contact_list_X_contacts_table, lazy="raise"
            )
        },
    )

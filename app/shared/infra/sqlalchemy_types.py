from typing import Any, Optional, Type
from uuid import UUID

from sqlalchemy import String, TypeDecorator
from sqlalchemy.sql.sqltypes import TypeEngine

from app.shared.domain.aggregate import DomainId


class DomainIdObjectType(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self, class_of_value_object: Type[DomainId], type: TypeEngine):
        self.class_of_value_object = class_of_value_object
        self.type = type
        super(DomainIdObjectType, self).__init__()

    def load_dialect_impl(self, dialect: Any) -> Any:
        return dialect.type_descriptor(self.type)

    def process_bind_param(
        self, value_object: Optional[DomainId], dialect: Any
    ) -> UUID:
        value: UUID
        if value_object is not None:
            value = value_object.value
        return value

    def process_result_value(self, value: Optional[UUID], dialect: Any) -> DomainId:
        if value is not None:
            value_object = self.class_of_value_object(value)
        return value_object

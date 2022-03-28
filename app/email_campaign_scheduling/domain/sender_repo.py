from typing import Optional, Protocol, Type
from .sender import Sender, SenderId
from app.shared.infra.db import MySQLRepo


class SenderRepo(Protocol):
    def store(self, user: Sender) -> None:
        raise NotImplementedError

    def update(self, user: Sender) -> None:
        raise NotImplementedError

    def find_by_id(self, id: SenderId) -> Optional[Sender]:
        raise NotImplementedError


class SenderMySQLRepo(MySQLRepo[Sender, SenderId]):
    def store(self, user: Sender) -> None:
        super()._save(user)

    def update(self, user: Sender) -> None:
        super()._save(user)

    def find_by_id(self, id: SenderId) -> Optional[Sender]:
        return super()._find_by_id(id)

    @property
    def _clz(self) -> Type[Sender]:
        return Sender


sender_mysql_repo = SenderMySQLRepo()

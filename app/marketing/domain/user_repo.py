from typing import Optional, Protocol, Type

from app.shared.infra.db import MySQLRepo

from .user import User, UserId


class UserRepo(Protocol):
    def store(self, user: User) -> None:
        raise NotImplementedError

    def update(self, user: User) -> None:
        raise NotImplementedError

    def find_by_id(self, id: UserId) -> Optional[User]:
        raise NotImplementedError


class UserMySQLRepo(MySQLRepo[User, UserId]):
    def store(self, user: User) -> None:
        super()._save(user)

    def update(self, user: User) -> None:
        super()._save(user)

    def find_by_id(self, id: UserId) -> Optional[User]:
        return super()._find_by_id(id)

    @property
    def _clz(self) -> Type[User]:
        return User


user_mysql_repo = UserMySQLRepo()

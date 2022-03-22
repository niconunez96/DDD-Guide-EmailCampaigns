from typing import Protocol
from .user import User, UserId
from app.shared.infra.db import MySQLRepo


class UserRepo(Protocol):
    def store(self, user: User) -> None:
        raise NotImplementedError

    def update(self, user: User) -> None:
        raise NotImplementedError


class UserMySQLRepo(MySQLRepo[User, UserId]):
    def store(self, user: User) -> None:
        super()._save(user)

    def update(self, user: User) -> None:
        super()._save(user)

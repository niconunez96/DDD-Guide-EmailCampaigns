from app.marketing.domain.user import UserId, User
from app.marketing.domain.user_repo import UserRepo
from ..domain.user_repo import user_mysql_repo


def create_user(id: UserId, user_repo: UserRepo = user_mysql_repo) -> None:
    user = User(id)
    user_repo.store(user)

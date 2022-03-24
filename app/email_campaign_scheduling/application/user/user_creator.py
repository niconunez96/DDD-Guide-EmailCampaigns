from app.email_campaign_scheduling.domain.user import UserId, User
from app.email_campaign_scheduling.domain.user_repo import UserRepo, user_mysql_repo


def create_user(id: UserId, user_repo: UserRepo = user_mysql_repo) -> None:
    user = User(id)
    user_repo.store(user)

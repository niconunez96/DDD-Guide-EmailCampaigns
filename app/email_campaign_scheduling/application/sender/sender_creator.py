from app.email_campaign_scheduling.domain.sender import SenderId, Sender
from app.email_campaign_scheduling.domain.sender_repo import UserRepo, user_mysql_repo


def create_sender(id: SenderId, user_repo: UserRepo = user_mysql_repo) -> None:
    user = Sender(id)
    user_repo.store(user)

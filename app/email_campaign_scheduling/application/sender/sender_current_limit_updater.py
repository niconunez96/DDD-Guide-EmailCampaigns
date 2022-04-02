from app.email_campaign_scheduling.domain.sender import SenderId
from app.email_campaign_scheduling.domain.sender_repo import (
    SenderRepo,
    sender_mysql_repo,
)


def update_sender_current_limit(
    id: SenderId, total_used: int, sender_repo: SenderRepo = sender_mysql_repo
) -> None:
    sender = sender_repo.find_by_id(id)
    if not sender:
        raise Exception("SENDER_NOT_FOUND")
    sender.update_current_limit(total_used)
    sender_repo.update(sender)

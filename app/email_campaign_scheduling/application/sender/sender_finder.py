from typing import Optional

from app.email_campaign_scheduling.domain.sender import SenderId, SenderResponse
from app.email_campaign_scheduling.domain.sender_repo import (
    SenderRepo,
    sender_mysql_repo,
)


def find_sender(
    id: SenderId, sender_repo: SenderRepo = sender_mysql_repo
) -> Optional[SenderResponse]:
    sender = sender_repo.find_by_id(id)
    return sender.to_response if sender else None

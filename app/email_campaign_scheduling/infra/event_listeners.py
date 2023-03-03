from logging import getLogger

from app.email_campaign_scheduling.application.sender import (
    sender_creator,
    sender_daily_send_limit_updater,
)
from app.email_campaign_scheduling.domain.sender import SenderId
from app.marketing.domain.user import UserCreated, UserPlanDowngraded, UserPlanUpgraded
from app.shared.domain.event_bus import EventListener

logger = getLogger("email_campaign_scheduling:event_listeners")


class UserCreatedListener(EventListener[UserCreated]):
    def listen(self, event: UserCreated) -> None:
        id = SenderId.from_string(event.user_id)
        if not id:
            logger.warn(f"User id: {id} is malformed")
            return
        sender_creator.create_sender(id)


class UserDowngradedListener(EventListener[UserPlanDowngraded]):
    def listen(self, event: UserPlanDowngraded) -> None:
        id = SenderId.from_string(event.user_id)
        if not id:
            logger.warn(f"User id: {id} is malformed")
            return
        sender_daily_send_limit_updater.update_daily_send_limit(id, event.plan)


class UserUpgradedListener(EventListener[UserPlanUpgraded]):
    def listen(self, event: UserPlanUpgraded) -> None:
        id = SenderId.from_string(event.user_id)
        if not id:
            logger.warn(f"User id: {id} is malformed")
            return
        sender_daily_send_limit_updater.update_daily_send_limit(id, event.plan)

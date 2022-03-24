from logging import getLogger
from app.email_campaign_scheduling.domain.user import UserId
from app.shared.domain.event_bus import EventListener
from app.marketing.domain.user import UserCreated, UserPlanUpgraded, UserPlanDowngraded
from app.email_campaign_scheduling.application.user import (
    user_creator,
    user_daily_send_limit_updater,
)

logger = getLogger("email_campaign_scheduling:event_listeners")


class UserCreatedListener(EventListener[UserCreated]):
    def listen(self, event: UserCreated) -> None:
        id = UserId.from_string(event.user_id)
        if not id:
            logger.warn(f"User id: {id} is malformed")
            return
        user_creator.create_user(id)


class UserDowngradedListener(EventListener[UserPlanDowngraded]):
    def listen(self, event: UserPlanDowngraded) -> None:
        id = UserId.from_string(event.user_id)
        if not id:
            logger.warn(f"User id: {id} is malformed")
            return
        user_daily_send_limit_updater.update_daily_send_limit(id, event.plan)


class UserUpgradedListener(EventListener[UserPlanUpgraded]):
    def listen(self, event: UserPlanUpgraded) -> None:
        id = UserId.from_string(event.user_id)
        if not id:
            logger.warn(f"User id: {id} is malformed")
            return
        user_daily_send_limit_updater.update_daily_send_limit(id, event.plan)

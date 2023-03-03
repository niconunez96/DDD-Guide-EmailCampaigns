from app.marketing.domain.user import User, UserId
from app.marketing.domain.user_repo import UserRepo
from app.shared.domain.event_bus import EventBus

from ..domain.user_repo import user_mysql_repo


def create_user(
    id: UserId, event_bus: EventBus, user_repo: UserRepo = user_mysql_repo
) -> None:
    user = User(id)
    user_repo.store(user)
    event_bus.publish(*user.events)

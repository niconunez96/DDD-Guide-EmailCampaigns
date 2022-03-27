from ..domain.event_bus import InMemoryEventBus
from app.marketing.domain.user import UserCreated, UserPlanDowngraded, UserPlanUpgraded
from app.email_campaign_scheduling.infra.event_listeners import (
    UserDowngradedListener,
    UserCreatedListener,
    UserUpgradedListener,
)


in_memory_event_bus = InMemoryEventBus()


def init_event_listeners() -> None:
    in_memory_event_bus.register(UserCreated, [UserCreatedListener()])
    in_memory_event_bus.register(UserPlanUpgraded, [UserUpgradedListener()])
    in_memory_event_bus.register(UserPlanDowngraded, [UserDowngradedListener()])

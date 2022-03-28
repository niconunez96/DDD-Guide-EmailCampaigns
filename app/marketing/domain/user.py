from dataclasses import dataclass
from enum import Enum
from typing import Literal, cast
from uuid import UUID, uuid4
from app.shared.domain.aggregate import DomainId
from app.shared.domain.event_bus import DomainEvent


PlanType = Literal["REGULAR", "PREMIUM", "SUPER_SUPER_PREMIUM"]


@dataclass(frozen=True)
class UserCreated(DomainEvent):
    user_id: str
    _id: UUID = uuid4()

    @property
    def id(self) -> str:
        return str(self._id)

    @staticmethod
    def name() -> str:
        return "USER_CREATED"


@dataclass(frozen=True)
class UserPlanUpgraded(DomainEvent):
    user_id: str
    plan: PlanType
    _id: UUID = uuid4()

    @property
    def id(self) -> str:
        return str(self._id)

    @staticmethod
    def name() -> str:
        return "USER_PLAN_UPGRADED"


@dataclass(frozen=True)
class UserPlanDowngraded(DomainEvent):
    user_id: str
    plan: PlanType
    _id: UUID = uuid4()

    @property
    def id(self) -> str:
        return str(self._id)

    @staticmethod
    def name() -> str:
        return "USER_PLAN_DOWNGRADED"


class MarketingPlan(Enum):
    REGULAR = 1
    PREMIUM = 2
    SUPER_SUPER_PREMIUM = 3


class UserId(DomainId):
    pass


class User:
    id: UserId
    _plan: MarketingPlan
    events: list[UserPlanUpgraded | UserPlanDowngraded | UserCreated]

    def __init__(self, id: UserId) -> None:
        self.id = id
        self._plan = MarketingPlan.REGULAR
        self.events = []
        self.events.append(UserCreated(str(self.id)))

    def upgrade_plan(self, to_plan: MarketingPlan) -> None:
        if self._plan.value > to_plan.value:
            raise Exception("CANNOT_UPGRADE")
        self._plan = to_plan
        self.events.append(
            UserPlanUpgraded(str(self.id), cast(PlanType, self._plan.name))
        )

    def downgrade_plan(self, to_plan: MarketingPlan) -> None:
        if self._plan.value < to_plan.value:
            raise Exception("CANNOT_DOWNGRADE")
        self._plan = to_plan
        self.events.append(
            UserPlanDowngraded(str(self.id), cast(PlanType, self._plan.name))
        )

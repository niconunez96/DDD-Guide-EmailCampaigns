from enum import Enum
from typing import Literal
from app.shared.domain import DomainId


class MarketingPlan(Enum):
    REGULAR = 1
    PREMIUM = 2
    SUPER_SUPER_PREMIUM = 3


class UserId(DomainId):
    pass


class User:
    id: UserId
    _plan: MarketingPlan

    def __init__(self, id: UserId) -> None:
        self.id = id
        self._plan = MarketingPlan.REGULAR

    def upgrade_plan(self, to_plan: MarketingPlan) -> None:
        if self._plan.value > to_plan.value:
            raise Exception("CANNOT_UPGRADE")
        self._plan = to_plan

    def downgrade_plan(self, to_plan: MarketingPlan) -> None:
        if self._plan.value < to_plan.value:
            raise Exception("CANNOT_DOWNGRADE")
        self._plan = to_plan

from typing import Literal
from app.shared.domain.aggregate import DomainId


DailySendLimit = Literal[2000, 4000, 6000]

MarketingPlan = Literal["REGULAR", "PREMIUM", "SUPER_SUPER_PREMIUM"]


class SenderId(DomainId["SenderId"]):
    pass


class Sender:
    id: SenderId
    daily_send_limit: DailySendLimit
    daily_send_limit_per_plan: dict[MarketingPlan, DailySendLimit] = {
        "REGULAR": 2000,
        "PREMIUM": 4000,
        "SUPER_SUPER_PREMIUM": 6000,
    }

    def __init__(self, id: SenderId) -> None:
        self.id = id
        self.daily_send_limit = 2000

    def update_daily_send_limit(self, new_user_marketing_plan: MarketingPlan) -> None:
        self.daily_send_limit = self.daily_send_limit_per_plan[new_user_marketing_plan]

from datetime import date, datetime, timedelta
from typing import Literal, Optional, TypedDict
from app.shared.domain.aggregate import DomainId


DailySendLimit = Literal[2000, 4000, 6000]

MarketingPlan = Literal["REGULAR", "PREMIUM", "SUPER_SUPER_PREMIUM"]


class SenderResponse(TypedDict):
    id: str
    daily_send_limit: int
    current_limit: int


class SenderId(DomainId["SenderId"]):
    pass


class Sender:
    id: SenderId
    daily_send_limit: DailySendLimit
    _current_limit: int
    _last_time_current_limit_was_updated: Optional[date]
    daily_send_limit_per_plan: dict[MarketingPlan, DailySendLimit] = {
        "REGULAR": 2000,
        "PREMIUM": 4000,
        "SUPER_SUPER_PREMIUM": 6000,
    }

    def __init__(self, id: SenderId) -> None:
        self.id = id
        self.daily_send_limit = 2000
        self._current_limit = self.daily_send_limit

    def update_daily_send_limit(self, new_user_marketing_plan: MarketingPlan) -> None:
        self.daily_send_limit = self.daily_send_limit_per_plan[new_user_marketing_plan]

    def update_current_limit(self, total_used: int) -> None:
        self._current_limit = self.daily_send_limit - total_used
        self._last_time_current_limit_was_updated = datetime.now().date()

    @property
    def current_limit(self) -> int:
        if (
            self._last_time_current_limit_was_updated
            and self._last_time_current_limit_was_updated - datetime.now().date()
            > timedelta(days=1)
        ):
            return self.daily_send_limit
        return self._current_limit

    @property
    def to_response(self) -> SenderResponse:
        return {
            "id": str(self.id),
            "daily_send_limit": self.daily_send_limit,
            "current_limit": self.current_limit,
        }

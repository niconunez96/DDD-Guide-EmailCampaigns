from app.email_campaign_scheduling.domain.sender import MarketingPlan, SenderId
from app.email_campaign_scheduling.domain.sender_repo import UserRepo, user_mysql_repo


def update_daily_send_limit(
    id: SenderId, new_plan: MarketingPlan, user_repo: UserRepo = user_mysql_repo
) -> None:
    user = user_repo.find_by_id(id)
    if not user:
        raise Exception("USER_NOT_FOUND")
    user.update_daily_send_limit(new_plan)
    user_repo.update(user)

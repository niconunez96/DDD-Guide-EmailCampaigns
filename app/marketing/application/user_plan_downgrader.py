from typing import NoReturn
from ..domain.user import UserId, MarketingPlan
from ..domain.user_repo import UserRepo, user_mysql_repo


def downgrade_user_plan(
    user_id: UserId, new_plan: MarketingPlan, user_repo: UserRepo = user_mysql_repo
) -> None:
    user = user_repo.find_by_id(user_id)
    if not user:
        raise Exception("USER_NOT_FOUND")
    user.downgrade_plan(new_plan)
    user_repo.update(user)

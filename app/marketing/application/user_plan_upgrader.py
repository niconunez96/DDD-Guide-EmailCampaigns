from typing import NoReturn
from ..domain.user import UserId, MarketingPlan
from ..domain.user_repo import UserRepo, user_mysql_repo


def upgrade_user_plan(
    user_id: UserId, new_plan: MarketingPlan, user_repo: UserRepo = user_mysql_repo
) -> None:
    user = user_repo.find_by_id(user_id)
    if not user:
        raise Exception("User not found")
    user.upgrade_plan(new_plan)
    user_repo.update(user)


# class UserPlanUpgrader:
#     def __init__(self, user_repo: UserRepo = user_mysql_repo) -> None:
#         self.user_repo = user_repo

#     def __call__(self, user_id: UserId, new_plan: MarketingPlan) -> None:
#         user = self.user_repo.find_by_id(user_id)
#         if not user:
#             raise Exception("User not found")
#         user.upgrade_plan(new_plan)
#         self.user_repo.update(user)

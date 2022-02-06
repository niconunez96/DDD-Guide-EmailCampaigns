from typing import Protocol
from .campaign import Campaign


class CampaignRepo(Protocol):
    def save(self, campaign: Campaign) -> None:
        raise NotImplementedError

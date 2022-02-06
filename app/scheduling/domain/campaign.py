from typing import NewType
from uuid import UUID

CampaignId = NewType("CampaignId", UUID)


class Campaign:
    id: CampaignId
    _name: str
    _subject: str
    _body: str
    _sender: str

    def __init__(self, id: CampaignId, name: str, subject: str, body: str, sender: str):
        self.id = id
        self._name = name
        self._subject = subject
        self._body = body
        self._sender = sender

    def __str__(self) -> str:
        return f"Campaign {self._name}"

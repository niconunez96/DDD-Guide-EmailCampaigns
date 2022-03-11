from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypedDict
from uuid import UUID

from app.shared.domain import DomainId


class CampaignResponse(TypedDict):
    id: str
    name: str
    subject: str
    body: str
    sender: str
    schedule_datetime: str


@dataclass(frozen=True)
class CampaignId(DomainId):
    _id: UUID

    @staticmethod
    def from_string(id: str) -> CampaignId:
        return CampaignId(UUID(id))

    @property
    def value(self) -> UUID:
        return self._id


class Campaign:
    id: CampaignId
    _name: str
    _subject: str
    _body: str
    _sender: str
    _schedule_datetime: Optional[datetime] = None

    def __init__(self, id: CampaignId, name: str, subject: str, body: str, sender: str):
        self.id = id
        self._name = name
        self._subject = subject
        self._body = body
        self._sender = sender

    def __str__(self) -> str:
        return f"Campaign {self._name}"

    def to_response(self) -> CampaignResponse:
        return {
            "id": str(self.id),
            "name": self._name,
            "subject": self._subject,
            "body": self._body,
            "sender": self._sender,
            "schedule_datetime": self._schedule_datetime.isoformat() if self._schedule_datetime else "",
        }

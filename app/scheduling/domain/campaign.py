from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional, TypedDict
from uuid import UUID

from app.shared.domain import DomainId


CAMPAIGN_STATUS = Literal[
    "DRAFT",
    "SCHEDULED",
    "SENDING",
    "SENT",
]


class CampaignResponse(TypedDict):
    id: str
    name: str
    subject: str
    body: str
    sender: str
    schedule_datetime: str
    status: str


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
    _status: CAMPAIGN_STATUS

    def __init__(self, id: CampaignId, name: str, subject: str, body: str, sender: str):
        self.id = id
        self._name = name
        self._subject = subject
        self._body = body
        self._sender = sender
        self._status = "DRAFT"

    def __str__(self) -> str:
        return f"Campaign {self._name}"

    def to_response(self) -> CampaignResponse:
        return {
            "id": str(self.id),
            "name": self._name,
            "subject": self._subject,
            "body": self._body,
            "sender": self._sender,
            "schedule_datetime": self._schedule_datetime.isoformat()
            if self._schedule_datetime
            else "",
            "status": self._status,
        }

    def _is_valid_status_transition(
        self, current_status: CAMPAIGN_STATUS, next_status: CAMPAIGN_STATUS
    ) -> bool:
        transitions: dict[CAMPAIGN_STATUS, list[CAMPAIGN_STATUS]] = {
            "DRAFT": ["SCHEDULED", "SENDING"],
            "SCHEDULED": ["SENDING", "DRAFT"],
            "SENDING": [],
            "SENT": [],
        }
        return next_status in transitions.get(current_status, [])

    def mark_as_scheduled(self, schedule_datetime: datetime) -> None:
        if not self._is_valid_status_transition(self._status, "SCHEDULED"):
            raise Exception("Cannot schedule a campaign that has status" + self._status)
        self._schedule_datetime = schedule_datetime
        self._status = "SCHEDULED"

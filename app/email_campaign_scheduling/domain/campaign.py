from datetime import datetime, timedelta
from typing import Literal, NamedTuple, Optional, TypedDict

from app.email_campaign_scheduling.domain.contact_list import ContactList, ContactListId
from app.email_campaign_scheduling.domain.sender import SenderId
from app.shared.domain.aggregate import DomainId

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


class ContactListTarget:
    id: int
    contact_list_id: ContactListId
    quantity_sent: int

    def __init__(self, contact_list_id: ContactListId) -> None:
        self.contact_list_id = contact_list_id
        self.quantity_sent = 0

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, ContactListTarget):
            return False
        return self.contact_list_id == __o.contact_list_id

    def __hash__(self) -> int:
        return hash(self.contact_list_id)


class ContactListToSend(NamedTuple):
    contact_list_id: ContactListId
    quantity_limit: int


class ContactListsToSend(NamedTuple):
    contact_lists: list[ContactListToSend]
    should_reschedule_campaign: bool


class CampaignId(DomainId["CampaignId"]):
    pass


class Campaign:
    id: CampaignId
    _name: str
    _subject: str
    _body: str
    _sender_email: str
    _schedule_datetime: Optional[datetime] = None
    _status: CAMPAIGN_STATUS
    _sender_id: SenderId
    _contact_list_targets: set[ContactListTarget]

    def __init__(
        self,
        id: CampaignId,
        name: str,
        subject: str,
        body: str,
        sender_email: str,
        sender_id: SenderId,
    ) -> None:
        self.id = id
        self._name = name
        self._subject = subject
        self._body = body
        self._sender_email = sender_email
        self._status = "DRAFT"
        self._sender_id = sender_id
        self._contact_list_targets = set()

    def __str__(self) -> str:
        return f"Campaign {self._name}"

    def to_response(self) -> CampaignResponse:
        return {
            "id": str(self.id),
            "name": self._name,
            "subject": self._subject,
            "body": self._body,
            "sender": self._sender_email,
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
            "SENDING": ["SENT"],
            "SENT": [],
        }
        return next_status in transitions.get(current_status, [])

    def schedule(self, schedule_datetime: datetime) -> None:
        if not self._is_valid_status_transition(self._status, "SCHEDULED"):
            raise Exception("Cannot schedule a campaign that has status" + self._status)
        self._schedule_datetime = schedule_datetime
        self._status = "SCHEDULED"

    def add_contact_lists(self, contact_lists: list[ContactList]) -> None:
        if self._status != "DRAFT":
            raise Exception("CANNOT_ADD_CONTACT_LISTS_TO_NON_DRAFT_CAMPAIGN")
        if not all(
            self._sender_id == contact_list._user_id for contact_list in contact_lists
        ):
            raise Exception("USER_ID_MISMATCH")
        new_contact_list_targets = {
            ContactListTarget(
                contact_list_id=contact_list.id,
            )
            for contact_list in contact_lists
        }
        self._contact_list_targets.update(new_contact_list_targets)

    def calculate_contact_lists_to_send(
        self, daily_send_limit: int, contact_lists: list[ContactList]
    ) -> ContactListsToSend:
        if daily_send_limit == 0:
            return ContactListsToSend([], should_reschedule_campaign=True)
        contacts_quantity = 0
        contact_lists_to_send = []

        contact_list_targets = sorted(
            self._contact_list_targets, key=lambda x: x.contact_list_id
        )
        contact_lists_sorted = sorted(contact_lists, key=lambda cl: cl.id)

        for (contact_list_target, contact_list) in zip(
            contact_list_targets, contact_lists_sorted
        ):
            if contact_list_target.quantity_sent == contact_list._contacts_quantity:
                continue
            contacts_quantity += contact_list._contacts_quantity
            if contacts_quantity > daily_send_limit:
                contact_lists_to_send.append(
                    ContactListToSend(
                        contact_list.id, abs(daily_send_limit - contacts_quantity)
                    )
                )
                return ContactListsToSend(
                    contact_lists_to_send, should_reschedule_campaign=True
                )
            contact_lists_to_send.append(
                ContactListToSend(contact_list.id, contact_list._contacts_quantity)
            )
        return ContactListsToSend(contact_lists_to_send, should_reschedule_campaign=False)

    def start_sending(self) -> None:
        if not self._is_valid_status_transition(self._status, "SENDING"):
            raise Exception("CANNOT_START_SENDING")
        self._status = "SENDING"

    def mark_as_sent(self) -> None:
        if not self._is_valid_status_transition(self._status, "SENT"):
            raise Exception("CANNOT_MARK_AS_SENT")
        self._status = "SENT"

    def schedule_for_tomorrow(
        self, contact_lists_sent: dict[ContactListId, int]
    ) -> None:
        self._schedule_datetime = datetime.now() + timedelta(days=1)
        self._status = "SCHEDULED"
        for contact_list_target in self._contact_list_targets:
            id = contact_list_target.contact_list_id
            if id not in contact_lists_sent.keys():
                continue
            contact_list_target.quantity_sent += contact_lists_sent.get(id, 0)

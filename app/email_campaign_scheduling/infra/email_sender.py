from logging import getLogger
import os
from typing import Iterator, Protocol, TypedDict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, CustomArg, Email


class Message(TypedDict):
    subject: str
    body: str
    sender_email: str
    campaign_id: str
    sender_id: str
    recipient_emails: Iterator[str]


class EmailSender(Protocol):
    def send_emails(self, message: Message) -> None:
        raise NotImplementedError


class SendgridEmailSender:
    def __init__(self) -> None:
        self.logger = getLogger(self.__class__.__name__)

    def send_emails(self, message: Message) -> None:
        email = Mail(
            from_email="nicolas110996@gmail.com",
            subject=message["subject"],
            html_content=message["body"],
        )
        email.reply_to = message["sender_email"]
        for recipient in message["recipient_emails"]:
            pers = Personalization()
            pers.add_to(Email(recipient))
            pers.add_custom_arg(CustomArg("campaign_id", message["campaign_id"]))
            pers.add_custom_arg(CustomArg("sender_id", message["sender_id"]))
            email.add_personalization(pers)
        try:
            sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
            sg.send(email)
        except Exception as e:
            self.logger.error(e)
            raise e


sendgrid_email_sender = SendgridEmailSender()

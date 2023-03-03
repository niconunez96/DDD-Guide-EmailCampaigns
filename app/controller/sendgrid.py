import logging
import os
from http import HTTPStatus

from flask import Blueprint, Response, jsonify, request

sengrid_endpoint = Blueprint("sengrid_endpoint", __name__)


logger = logging.getLogger(__name__)


@sengrid_endpoint.route("/send_example/", methods=["POST"])
def send() -> tuple[Response, HTTPStatus]:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import CustomArg, Email, Mail, Personalization

    message = Mail(
        from_email="nicolas110996@gmail.com",
        to_emails="nicolas110996@gmail.com",
        subject="Sending with Twilio SendGrid is Fun",
        html_content="<strong>and easy to do anywhere, even with Python</strong>",
    )
    pers = Personalization()
    pers.add_to(Email("nicolas110996@gmail.com"))
    pers.add_custom_arg(CustomArg("campaign_id", "12345"))
    message.add_personalization(pers)
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
        return jsonify("OK"), HTTPStatus.OK
    except Exception as e:
        logger.error(e)
        return jsonify(e.body), HTTPStatus.BAD_REQUEST  # type: ignore


@sengrid_endpoint.route("/sendgrid_activities/", methods=["POST"])
def sendgrid_activities() -> tuple[Response, HTTPStatus]:
    body = request.data
    logger.info(body)
    return jsonify({"data": "OK"}), HTTPStatus.OK

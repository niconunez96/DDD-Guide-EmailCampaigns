from datetime import datetime
import logging
import os
from typing import Optional
import uuid
from http import HTTPStatus

from flask import Blueprint, Response, jsonify, request

from app.scheduling.domain.campaign import CampaignId

from .scheduling.application.campaign_creator import (
    CreateCampaignCommand,
    create_campaign,
)
from .scheduling.application.campaign_finder import find_campaign
from .scheduling.application.campaign_scheduler import (
    ScheduleCommand,
    schedule_campaign,
)
from .scheduling.domain.campaign_repo import campaign_mysql_repo

sengrid_endpoint = Blueprint("sengrid_endpoint", __name__)
campaign_endpoint = Blueprint("dummy", __name__, url_prefix="/campaigns")


@campaign_endpoint.route("/<string:id>/", methods=["GET"])
def find(id: str) -> tuple[Response, HTTPStatus]:
    campaign_id = CampaignId.from_string(id)
    if not campaign_id:
        return jsonify({"error": "NOT_FOUND"}), HTTPStatus.NOT_FOUND
    campaign = find_campaign(campaign_id)
    if not campaign:
        return jsonify({"error": "NOT_FOUND"}), HTTPStatus.NOT_FOUND
    return jsonify({"data": campaign}), HTTPStatus.OK


@campaign_endpoint.route("/<string:id>/schedule/", methods=["POST"])
def schedule(id: str) -> tuple[Response, HTTPStatus]:
    campaign_id = CampaignId.from_string(id)
    if not campaign_id:
        return jsonify({"error": "NOT_FOUND"}), HTTPStatus.NOT_FOUND
    data: Optional[dict[str, str]] = request.json
    if not data:
        return jsonify({"error": "MISSING_DATA"}), HTTPStatus.BAD_REQUEST
    try:
        schedule_campaign(
            ScheduleCommand(
                campaign_id,
                datetime.strptime(data["schedule_datetime"], "%Y-%m-%d %H:%M"),
            ),
        )
    except:
        return jsonify({"error": "NOT_FOUND"}), HTTPStatus.NOT_FOUND
    return jsonify({}), HTTPStatus.ACCEPTED


@campaign_endpoint.route("/", methods=["POST"])
def create() -> tuple[Response, HTTPStatus]:
    id = uuid.uuid4()
    data = request.json
    if not data:
        return jsonify({"error": "MISSING_DATA"}), HTTPStatus.BAD_REQUEST
    create_campaign(
        CreateCampaignCommand(
            id, data["name"], data["subject"], data["body"], data["sender"]
        ),
    )
    return jsonify({"data": {"id": id}}), HTTPStatus.CREATED


@campaign_endpoint.route("/send_example/", methods=["POST"])
def send() -> tuple[Response, HTTPStatus]:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Personalization, CustomArg, Email

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
        sg = SendGridAPIClient(
            os.getenv("SENDGRID_API_KEY")
        )
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        return jsonify("OK"), HTTPStatus.OK
    except Exception as e:
        print(e)
        return jsonify(e.body), HTTPStatus.BAD_REQUEST  # type: ignore


@sengrid_endpoint.route("/sendgrid_activities/", methods=["POST"])
def sendgrid_activities() -> tuple[Response, HTTPStatus]:
    body = request.data
    logging.getLogger().info(body)
    return jsonify({"data": "OK"}), HTTPStatus.OK

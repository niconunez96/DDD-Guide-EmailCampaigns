from datetime import datetime
from typing import Optional
import uuid
from http import HTTPStatus

from flask import Blueprint, Response, jsonify, request

from app.email_campaign_scheduling.domain.campaign import CampaignId

from app.email_campaign_scheduling.application.campaign_creator import (
    CreateCampaignCommand,
    create_campaign,
)
from app.email_campaign_scheduling.application.campaign_finder import find_campaign
from app.email_campaign_scheduling.application.campaign_scheduler import (
    ScheduleCommand,
    schedule_campaign,
)

campaign_endpoint = Blueprint("campaign", __name__, url_prefix="/campaigns")


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

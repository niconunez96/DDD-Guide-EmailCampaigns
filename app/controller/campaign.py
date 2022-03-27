from datetime import datetime
from typing import Optional
import uuid
from http import HTTPStatus

from flask import Blueprint, Response, jsonify, request

from app.email_campaign_scheduling.domain.campaign import CampaignId

from app.email_campaign_scheduling.application.campaign.campaign_creator import (
    CreateCampaignCommand,
    create_campaign,
)
from app.email_campaign_scheduling.application.campaign.campaign_finder import (
    find_campaign,
    find_user_campaigns,
)
from app.email_campaign_scheduling.application.campaign.campaign_scheduler import (
    ScheduleCommand,
    schedule_campaign,
)
from app.email_campaign_scheduling.application.campaign_contact_list_adder import (
    add_contact_lists,
    AddCampaignToContactListCommand,
)
from app.email_campaign_scheduling.domain.contact_list import ContactListId

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


@campaign_endpoint.route("/", methods=["GET"])
def find_by_user() -> tuple[Response, HTTPStatus]:
    id = request.args.get("user_id")
    if not id:
        return jsonify({"error": "NOT_FOUND"}), HTTPStatus.NOT_FOUND
    campaigns = find_user_campaigns(id)
    return jsonify({"data": campaigns}), HTTPStatus.OK


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
            id,
            data["name"],
            data["subject"],
            data["body"],
            data["sender"],
            data["user_id"],
        ),
    )
    return jsonify({"data": {"id": id}}), HTTPStatus.CREATED


@campaign_endpoint.route("/<string:id>/contact_lists/", methods=["POST"])
def add_cl(id: str) -> tuple[Response, HTTPStatus]:
    campaign_id = CampaignId.from_string(id)
    if not campaign_id:
        return jsonify({"error": "NOT_FOUND"}), HTTPStatus.NOT_FOUND
    data = request.json
    if not data:
        return jsonify({"error": "MISSING_DATA"}), HTTPStatus.BAD_REQUEST
    cl_ids = [
        ContactListId.from_string(cl_id) for cl_id in data.get("contact_list_ids", [])
    ]
    contact_list_ids = [id for id in cl_ids if id]
    try:
        add_contact_lists(AddCampaignToContactListCommand(campaign_id, contact_list_ids))
        return jsonify({}), HTTPStatus.ACCEPTED
    except Exception as e:
        match e:
            case "CAMPAIGN_NOT_FOUND": return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND
            case "CONTACT_LISTS_NOT_FOUND": return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
            case "USER_ID_MISMATCH": return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
            case _: return jsonify({"error": "UNKNOWN"}), HTTPStatus.INTERNAL_SERVER_ERROR

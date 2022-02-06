from http import HTTPStatus
import logging
from uuid import UUID
import uuid

from flask import Blueprint, Response, jsonify, request
from sqlalchemy.orm import scoped_session

from app.db import SessionFactory
from app.scheduling.domain.campaign import Campaign

from .scheduling.application.campaign_creator import (
    CreateCampaignCommand,
    create_campaign,
)
from .scheduling.domain.campaign_repo import campaign_mysql_repo

dummy_endpoint = Blueprint("dummy", __name__, url_prefix="/campaigns")


@dummy_endpoint.route("/<string:id>/", methods=["GET"])
def hello_world(id: str) -> tuple[Response, HTTPStatus]:
    campaign_id = UUID(id)
    session = scoped_session(SessionFactory)
    campaign = session.query(Campaign).filter_by(id=campaign_id).first()
    logger = logging.getLogger(__name__)
    logger.info(campaign)
    if not campaign:
        return jsonify({"error": "NOT_FOUND"}), HTTPStatus.NOT_FOUND
    return jsonify({"data": {"id": campaign.id, "name": campaign._name}}), HTTPStatus.OK


@dummy_endpoint.route("/", methods=["POST"])
def create() -> tuple[Response, HTTPStatus]:
    id = uuid.uuid4()
    data = request.json
    if not data:
        return jsonify({"error": "MISSING_DATA"}), HTTPStatus.BAD_REQUEST
    create_campaign(
        campaign_mysql_repo,
        CreateCampaignCommand(
            id, data["name"], data["subject"], data["body"], data["sender"]
        ),
    )
    return jsonify({"data": {"id": id}}), HTTPStatus.CREATED

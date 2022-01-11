from typing import Optional
from uuid import UUID, uuid4
from flask import Blueprint, jsonify
from sqlalchemy.orm import scoped_session
from app.db import SessionFactory
from app.model import Campaign

dummy_endpoint = Blueprint("dummy", __name__, url_prefix="/campaigns")


@dummy_endpoint.route("/<string:id>/", methods=["GET"])
def hello_world(id: str):
    campaign_id = UUID(id)
    session = scoped_session(SessionFactory)
    campaign = session.query(Campaign).filter_by(id=campaign_id).first()
    if not campaign:
        return jsonify({"error": "NOT_FOUND"}), 404
    return jsonify({"data": {"id": campaign.id}}), 200


@dummy_endpoint.route("/", methods=["POST"])
def create_campaign():
    campaign = Campaign(uuid4(), "some name", "some subject")
    session = scoped_session(SessionFactory)
    session.add(campaign)
    session.commit()
    return jsonify({"data": {"id": campaign.id}}), 201

import uuid
from http import HTTPStatus

from flask import Blueprint, Response, jsonify, request

from app.marketing.application import (
    create_user,
    downgrade_user_plan,
    upgrade_user_plan,
)
from app.marketing.domain.user import MarketingPlan, UserId
from app.shared.infra.event_bus import in_memory_event_bus

user_endpoint = Blueprint("user", __name__, url_prefix="/users")

plans = {
    "REGULAR": 1,
    "PREMIUM": 2,
    "SUPER_SUPER_PREMIUM": 3,
}


@user_endpoint.route("/", methods=["POST"])
def create() -> tuple[Response, HTTPStatus]:
    id = UserId(uuid.uuid4())
    create_user(id, in_memory_event_bus)
    return jsonify({"data": {"id": str(id)}}), HTTPStatus.CREATED


@user_endpoint.route("/<string:id>/upgrade_plan/", methods=["POST"])
def upgrade(id: str) -> tuple[Response, HTTPStatus]:
    user_id = UserId.from_string(id)
    if not user_id:
        return jsonify({"error": "INVALID_ID"}), HTTPStatus.BAD_REQUEST
    plan = (request.json or {}).get("plan", None)
    if not plan or plan not in plans:
        return jsonify({"error": "INVALID_PLAN"}), HTTPStatus.BAD_REQUEST
    try:
        upgrade_user_plan(user_id, MarketingPlan(plans[plan]), in_memory_event_bus)
    except Exception as e:
        match str(e):  # type: ignore
            case "USER_NOT_FOUND": return jsonify({"error": "NOT_FOUND"}), HTTPStatus.NOT_FOUND
            case "CANNOT_UPGRADE": return jsonify({"error": "CANNOT_UPGRADE"}), HTTPStatus.BAD_REQUEST
    return jsonify({}), HTTPStatus.ACCEPTED


@user_endpoint.route("/<string:id>/downgrade_plan/", methods=["POST"])
def downgrade(id: str) -> tuple[Response, HTTPStatus]:
    user_id = UserId.from_string(id)
    if not user_id:
        return jsonify({"error": "INVALID_ID"}), HTTPStatus.BAD_REQUEST
    plan = (request.json or {}).get("plan", None)
    if not plan or plan not in plans:
        return jsonify({"error": "INVALID_PLAN"}), HTTPStatus.BAD_REQUEST
    try:
        downgrade_user_plan(user_id, MarketingPlan(plans[plan]), in_memory_event_bus)
    except Exception as e:
        match str(e):  # type: ignore
            case "USER_NOT_FOUND": return jsonify({"error": "NOT_FOUND"}), HTTPStatus.NOT_FOUND
            case "CANNOT_DOWNGRADE": return jsonify({"error": "CANNOT_UPGRADE"}), HTTPStatus.BAD_REQUEST
            case _: return jsonify({"error": "UNKNOWN"}), HTTPStatus.INTERNAL_SERVER_ERROR
    return jsonify({}), HTTPStatus.ACCEPTED

import uuid
from http import HTTPStatus

from flask import Blueprint, Response, jsonify, request

from app.marketing.domain.user import UserId, MarketingPlan
from app.marketing.application import (
    create_user,
    upgrade_user_plan,
    downgrade_user_plan,
)

user_endpoint = Blueprint("user", __name__, url_prefix="/users")


@user_endpoint.route("/", methods=["POST"])
def create() -> tuple[Response, HTTPStatus]:
    id = UserId(uuid.uuid4())
    create_user(id)
    return jsonify({"data": {"id": str(id)}}), HTTPStatus.CREATED


@user_endpoint.route("/<string:id>/upgrade_plan/", methods=["POST"])
def upgrade(id: str) -> tuple[Response, HTTPStatus]:
    user_id = UserId.from_string(id)
    if not user_id:
        return jsonify({"error": "INVALID_ID"}), HTTPStatus.BAD_REQUEST
    try:
        upgrade_user_plan(user_id, MarketingPlan.PREMIUM)
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
    try:
        downgrade_user_plan(user_id, MarketingPlan.REGULAR)
    except Exception as e:
        match str(e):  # type: ignore
            case "USER_NOT_FOUND": return jsonify({"error": "NOT_FOUND"}), HTTPStatus.NOT_FOUND
            case "CANNOT_UPGRADE": return jsonify({"error": "CANNOT_UPGRADE"}), HTTPStatus.BAD_REQUEST
    return jsonify({}), HTTPStatus.ACCEPTED

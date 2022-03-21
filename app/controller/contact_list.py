from typing import Any, Optional
from uuid import uuid4
from flask import Response, jsonify, request
from http import HTTPStatus
from flask.blueprints import Blueprint
from app.scheduling.application.contact_list import (
    create_contact_list,
    CreateContactListCommand,
    find_contact_lists,
)
from app.scheduling.domain.contact_list import ContactListId

contact_list_endpoint = Blueprint(
    "contact_list_endpoint", __name__, url_prefix="/contact_lists"
)


@contact_list_endpoint.route("/", methods=["POST"])
def create() -> tuple[Response, HTTPStatus]:
    data: Optional[dict[str, Any]] = request.json
    if not data:
        return jsonify({"error": "MISSING DATA"}), HTTPStatus.BAD_REQUEST
    id = ContactListId(uuid4())
    cmd = CreateContactListCommand(
        id, data["name"], data["user_id"], data.get("contacts", [])
    )
    create_contact_list(cmd)
    return jsonify({"data": {"id": str(id)}}), HTTPStatus.ACCEPTED


@contact_list_endpoint.route("/<string:contact_list_id>/contacts/", methods=["GET"])
def get_contacts(contact_list_id: str) -> tuple[Response, HTTPStatus]:
    id = ContactListId.from_string(contact_list_id)
    if not id:
        return jsonify({"error": "INVALID ID"}), HTTPStatus.BAD_REQUEST
    contacts = find_contact_lists(id)
    return jsonify({"data": contacts}), HTTPStatus.OK

from flask import Blueprint


dummy_endpoint = Blueprint("dummy", __name__, url_prefix="/hello")


@dummy_endpoint.route("/", methods=["GET"])
def hello_world():
    return "Hello world"

from flask import Flask

from app.controller import campaign_endpoint
from app.shared.infra.db import init_db
from settings import init_logging

app = Flask(__name__)
app.register_blueprint(campaign_endpoint)


if __name__ == "__main__":
    init_db()
    init_logging()
    app.run(host="127.0.0.1", port=8080)

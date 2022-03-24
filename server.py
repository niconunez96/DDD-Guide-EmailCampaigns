from flask import Flask
from dotenv import load_dotenv

from app.controller import endpoints
from app.shared.infra.db import init_db
from app.shared.infra.event_bus import init_event_listeners
from settings import init_logging

load_dotenv()
app = Flask(__name__)
for endpoint in endpoints:
    app.register_blueprint(endpoint)


init_db()
init_logging()
init_event_listeners()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)

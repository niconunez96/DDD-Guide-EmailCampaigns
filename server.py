from flask import Flask
from dotenv import load_dotenv

from app.controller import campaign_endpoint
from app.shared.infra.db import init_db
from settings import init_logging

load_dotenv()
app = Flask(__name__)
app.register_blueprint(campaign_endpoint)


init_db()
init_logging()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)

from flask import Flask
from app.db import init_db
from app.controller import dummy_endpoint
from settings import init_logging

app = Flask(__name__)
app.register_blueprint(dummy_endpoint)


if __name__ == "__main__":
    init_db()
    init_logging()
    app.run(host="127.0.0.1", port=8080)

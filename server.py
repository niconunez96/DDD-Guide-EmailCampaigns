from flask import Flask

from app.controller import dummy_endpoint

app = Flask(__name__)
app.register_blueprint(dummy_endpoint)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)

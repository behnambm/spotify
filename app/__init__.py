from flask import Flask
from app.views.main import landing


def create_app() -> "Flask App":
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(landing.landing_bp)

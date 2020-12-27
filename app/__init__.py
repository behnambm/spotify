from flask import Flask
from app.views.main import landing
from app.views.spotify import authorize
from app.views.user import me, top_tracks
from app.auth import oauth
from app.errors import errors_bp
from app.models import db
from app.models.playlist import PlaylistModel
import os


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    oauth.init_app(app)
    register_blueprints(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///database.sqlite')
    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(landing.landing_bp)
    app.register_blueprint(authorize.auth_bp)
    app.register_blueprint(me.me_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(top_tracks.top_tracks_bp)

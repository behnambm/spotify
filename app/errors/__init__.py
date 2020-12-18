from flask import Blueprint, redirect, url_for
from flask_oauthlib.client import OAuthException

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(OAuthException)
def oauth_error(e):
    if 'No token available' in e.message:
        return redirect(url_for('landing.landing_page'))

    return 'hhh'

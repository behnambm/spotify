from flask import Blueprint, redirect, url_for, session, abort, flash
from flask_oauthlib.client import OAuthException
from urllib.error import URLError
from app.utils.errors import Unauthorized, TokenExpired
from app.utils import get_new_access_token

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(OAuthException)
def oauth_error(e):
    if 'No token available' in e.message:
        return redirect(url_for('landing.landing_page'))

    if e.data.get('error_description') == 'Invalid client secret':
        # add logging here
        flash('Server side error', 'error')
        return redirect(url_for('landing.landing_page'))

    return abort(500)


@errors_bp.app_errorhandler(URLError)
def internal_connection_error(e):
    flash('Internal server error.', 'error')
    # add logging here
    return redirect(url_for('landing.landing_page'))


@errors_bp.app_errorhandler(Unauthorized)
def handle_spotify_unauthorized_error(e):
    return {'message': e.message}, 401


@errors_bp.app_errorhandler(TokenExpired)
def refresh_expired_token(e):
    """
    This will handle the getting new access_token and redirecting to source endpoint
    """
    new_token = get_new_access_token()
    if new_token is None:
        abort(500)

    session['access_token'] = new_token
    # after getting get new token we need to redirect the user to the endpoint that
    # the token_expired` error was initiated
    return redirect(url_for(e.next_url))

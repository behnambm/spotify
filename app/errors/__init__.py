from flask import Blueprint, redirect, url_for, session, abort, flash
from flask_oauthlib.client import OAuthException
from urllib.error import URLError
from app.utils.errors import Unauthorized, TokenExpired
from app.auth import spotify
from app.utils import generate_basic_authorization_value
from os import getenv
from requests import post
import json

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
    This will handle the getting new access_token.
    sends a POST request to `spotify.access_token_url` and gets a new token
    using refresh token
    """
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': session.get('refresh_token')
    }
    authorization_value = generate_basic_authorization_value(
        consumer_id=getenv('SPOTIFY_CONSUMER_KEY'),
        consumer_secret=getenv('SPOTIFY_CONSUMER_SECRET')
    )
    header = {
        'Authorization': 'Basic ' + authorization_value.decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # use `requests` module to send the request
    resp = post(
        spotify.access_token_url,
        data=data,
        headers=header
    )

    if resp.status_code == 200:
        data = json.loads(resp.text)
        session['access_token'] = data.get('access_token')
        # after getting get new token we need to redirect the user to the endpoint that
        # the token_expired` error was initiated
        return redirect(url_for(e.next_url))

from flask import Blueprint, url_for, redirect, session, request, flash
from app.auth import spotify
from urllib.parse import urljoin, urlparse
import os


auth_bp = Blueprint('auth', __name__, url_prefix='/spotify')


@auth_bp.route('/authorize/')
def auth_user():
    """
    This endpoint will authorize the user and after that oauth-server will redirect the user
    to `callback` endpoint.
    """
    return spotify.authorize(callback=url_for('auth.auth_callback', _external=True))


@auth_bp.route('/authorize/callback/')
def auth_callback():
    """
    User after authorization will be redirected here and the request contains the authentication
    data. e.g. JWT, Expiration date, scope, etc.
    """
    resp = spotify.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return redirect(url_for('landing.landing_page'))

    session['access_token'] = resp.get('access_token')
    session['refresh_token'] = resp.get('refresh_token')
    return redirect(url_for('me.my_page'))


def add_version_to_api_url(uri, headers, body):
    """
    This function will execute before every request to the spotify's web api
    and adds the api version to the uri.

    In this app should be -> spotify.pre_request = add_version_to_api_url

    :param uri: url to the web api endpoint
    :param headers: a dict, containing headers like JWT
    :param body:
    """
    url = urlparse(uri)  # unpack the url
    endpoint = url.path

    proper_hostname = urljoin(
        url.scheme + '://' + url.hostname,  # generating the base url. e.g. https://example.com
        os.getenv('SPOTIFY_API_VERSION')
    )

    url_with_path = proper_hostname + endpoint
    return url_with_path, headers, body


# before every request to 'spotify' api this function will execute
spotify.pre_request = add_version_to_api_url

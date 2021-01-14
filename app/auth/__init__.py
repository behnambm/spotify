import os
from flask import session
from flask_oauthlib.client import OAuth


oauth = OAuth()

spotify = oauth.remote_app(
    'spotify',
    consumer_key=os.getenv('SPOTIFY_CONSUMER_KEY'),
    consumer_secret=os.getenv('SPOTIFY_CONSUMER_SECRET'),
    base_url='https://api.spotify.com/',
    request_token_url=None,
    authorize_url='https://accounts.spotify.com/authorize',
    access_token_url='https://accounts.spotify.com/api/token',
    request_token_params={'scope': 'user-read-email user-top-read playlist-modify-public'}
)


@spotify.tokengetter
def get_spotify_access_token() -> str:
    if 'access_token' in session:
        return session.get('access_token')

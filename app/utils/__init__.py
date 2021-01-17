from flask import session, flash, redirect, url_for, abort
from functools import wraps
from base64 import b64encode
from requests import post
import json
from typing import Union
from app.utils.errors import TokenExpired
from os import getenv
from app.auth import spotify


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('access_token') is None:
            flash('You need to sign-in first.', 'error')
            return redirect(url_for('landing.landing_page'))
        return f(*args, **kwargs)
    return wrapper


def calculate_track_duration(time_ms: int) -> str:
    """
    This converts the ms to s
    :param time_ms:
    :return: time in seconds
    """
    time_s = time_ms // 1000
    _min, _sec = divmod(time_s, 60)

    # convert to str
    _min = str(_min)
    _sec = str(_sec) if _sec > 9 else '0' + str(_sec)

    return ':'.join([_min, _sec])


def extract_tracks_data(tracks: dict) -> list:
    """
    this function extracts needed data for serialization
    :param tracks: a dict of tracks which spotify api returns
    :return: a list of dicts
    """
    tracks_list = []
    for item in tracks.get('items'):
        tmp_dict = dict()
        tmp_dict['track_name'] = item.get('name')
        tmp_dict['album_name'] = item.get('album').get('name')
        tmp_dict['track_uri'] = item.get('uri')
        tmp_dict['explicit'] = item.get('explicit')
        tmp_dict['track_duration'] = calculate_track_duration(item.get('duration_ms'))
        tmp_dict['artists_name'] = ', '.join([i['name'] for i in item.get('artists')])
        tracks_list.append(tmp_dict)

    return tracks_list


def generate_basic_authorization_value(consumer_id: str, consumer_secret: str) -> str:
    """
    According to spotify's documents `Authorization` parameter MUST have the following format.
    Authorization: Basic <base64 encoded client_id:client_secret>

    :param consumer_id:
    :param consumer_secret:
    :return:
    """
    proper_str = ':'.join([consumer_id, consumer_secret])
    return b64encode(proper_str.encode())


def create_playlist(name: str) -> Union[None, dict]:
    """
    This function will send a POST request to https://api.spotify.com/v1/users/{user_id}/playlists
    to create a new playlist.
    :return: useful parts of Spotify Playlist object
    """
    header = {
        'Authorization': 'Bearer ' + str(session.get('access_token')),
        'Content-Type': 'application/json'
    }

    data = {
        'name': name,
        'description': 'This playlist was imported from Spotify Taste (https://spotifytaste.herokuapp.com)'
    }
    try:
        resp = post(
            url=f'https://api.spotify.com/v1/users/{session.get("user_id")}/playlists',
            headers=header,
            data=json.dumps(data)
        )
    except Exception as e:
        # todo: add logging
        return None

    if resp.status_code == 200 or resp.status_code == 201:
        return json.loads(resp.text).get('id')

    if resp.status_code == 401:
        save_new_token_to_session()
        return create_playlist(name=name)

    return None


def add_tracks_to_playlist(track_uris: list, playlist_id) -> None:
    """
    This function will send a POST to https://api.spotify.com/v1/playlists/{playlist_id}/tracks
    to add items to new playlist the request contains list of track uris
    :param track_uris: a list of uris
    :param playlist_id: ID for new playlist
    """
    header = {
        'Authorization': 'Bearer ' + str(session.get('access_token')),
        'Content-Type': 'application/json'
    }

    data = {
        'uris': track_uris
    }
    try:
        resp = post(
            url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
            headers=header,
            data=json.dumps(data)
        )
    except Exception as e:
        # todo: add logging
        abort(500)

    if resp.status_code != 201:
        # todo: add loggin
        abort(500)


def get_new_access_token():
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
        return data.get('access_token')
    return None


def save_new_token_to_session():
    new_token = get_new_access_token()
    if new_token is None:
        abort(500)
    session['access_token'] = new_token
    return True

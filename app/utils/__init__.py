from flask import session, flash, redirect, url_for
from functools import wraps
from base64 import b64encode


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

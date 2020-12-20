from flask import session, flash, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('access_token') is None:
            flash('You need to log-in first.', 'error')
            return redirect(url_for('landing.landing_page')), 401
        return f(*args, **kwargs)
    return wrapper


def extract_tracks_data(tracks: dict) -> list:
    """
    this function extracts needed data for serialization
    :param tracks: a dict of tracks which spotify api returns
    :return: a list of dicts
    """
    tracks_list = []
    for item in tracks.get('items'):
        tmp_dict = {}
        tmp_dict['track_name'] = item.get('name')

        tracks_list.append(tmp_dict)

    return tracks_list

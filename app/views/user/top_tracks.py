"""
This endpoint is to get users top 10 tracks in a json format 
"""""
from flask import Blueprint, jsonify, abort
from app.auth import spotify
from app.schema.playlist import PlaylistSchema
from app.utils import extract_tracks_data

top_tracks_bp = Blueprint('top_tracks', __name__, url_prefix='/me/top/')
playlist_schema = PlaylistSchema(many=True)


@top_tracks_bp.route('/')
def get_top_tracks():
    """
    Retrieves user's top 20 songs in json format
    """
    tracks = spotify.get('me/top/tracks')

    tracks_data: list = extract_tracks_data(tracks.data)

    return playlist_schema.dump(tracks_data)

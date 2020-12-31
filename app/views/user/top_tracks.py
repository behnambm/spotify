"""
This endpoint is to get users top 10 tracks in a json format
"""
from flask import Blueprint, jsonify, request
from app.auth import spotify
from app.schema.playlist import PlaylistSchema
from app.utils import extract_tracks_data, login_required
from app.utils.errors import TokenExpired
from app.models import TracksModel

top_tracks_bp = Blueprint('top_tracks', __name__, url_prefix='/me/top/')
playlist_schema = PlaylistSchema(many=True)


@top_tracks_bp.route('/')
@login_required
def get_top_tracks():
    """
    Retrieves user's top 20 songs in json format
    Spotify's default count is 20
    """
    tracks = spotify.get('me/top/tracks')

    if tracks.status == 401:
        raise TokenExpired(next_url=request.endpoint)

    tracks_needed_data = extract_tracks_data(tracks.data)
    serialized_data = playlist_schema.dump(tracks_needed_data)

    for track in tracks_needed_data:
        # save all tracks to database
        TracksModel.check_and_save_to_db(track)

    return jsonify(serialized_data)

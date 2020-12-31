"""
This view is to save the tracks that user wants to share
"""
from flask import Blueprint, session, request
from app.utils import login_required
import json
from app.models import PlaylistModel, TracksModel


share_bp = Blueprint('share', __name__, url_prefix='/me/')


@share_bp.route('/share/', methods=['POST'])
@login_required
def share_tracks():
    user_uris = request.form.get('uris')
    if user_uris is None:
        return 'bad request', 400

    try:
        user_uris = json.loads(user_uris)
    except Exception:
        return 'bad request', 400

    if session.get('playlist_data') is None:
        return 'server error', 500

    new_playlist = PlaylistModel(
        playlist_name=session.get('display_name'),
        owner_user_id=session.get('user_id')
    )

    for uri in user_uris:
        new_playlist.tracks.append(TracksModel.find_by_uri(uri))

    new_playlist.save_to_db()
    print(new_playlist.tracks)

    return 'this will change', 201

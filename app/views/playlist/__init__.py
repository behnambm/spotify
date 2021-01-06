"""
This view is going to show playlists info
endpoint will be like this: /playlist/<PLAYLIST_ID>
"""
from flask import Blueprint, render_template, session, abort, url_for
from app.models import PlaylistModel
from app.schema.playlist import PlaylistSchema
from app.utils import login_required
import json

playlist_bp = Blueprint('playlist', __name__, url_prefix='/playlist/')
playlist_schema = PlaylistSchema(many=True)


@playlist_bp.route('/<playlist_id>')
def index(playlist_id: str):
    playlist = PlaylistModel.find_by_id_or_404(playlist_id)

    tracks = playlist_schema.dumps(playlist.tracks)
    # TODO: add `is_owner` flag, then user can edit playlist's name
    return render_template(
        'playlist.html',
        tracks=json.loads(tracks),
        playlist_name=playlist.playlist_name,
        avatar_url=playlist.playlist_image_url,
    )


@playlist_bp.route('/delete', methods=['DELETE'])
@login_required
def delete():
    user_playlist = PlaylistModel.find_by_user_id(session.get('user_id'))
    if not user_playlist:
        abort(404)

    user_playlist.delete_from_db()
    return url_for('me.my_page'), 200

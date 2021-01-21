"""
This view is going to show playlists info
endpoint will be like this: /playlist/<PLAYLIST_ID>
"""
from flask import Blueprint, render_template, session, abort, url_for, request, jsonify
from app.models import PlaylistModel
from app.schema.playlist import PlaylistSchema
from app.utils import login_required, create_playlist, add_tracks_to_playlist
import json

playlist_bp = Blueprint('playlist', __name__, url_prefix='/playlist/')
playlist_schema = PlaylistSchema(many=True)


@playlist_bp.route('/<playlist_id>')
def index(playlist_id: str):
    playlist = PlaylistModel.find_by_id_or_404(playlist_id)

    tracks = playlist_schema.dumps(playlist.tracks)

    is_owner = False
    if playlist.owner_user_id == session.get('user_id'):
        is_owner = True

    return render_template(
        'playlist.html',
        tracks=json.loads(tracks),
        playlist_name=playlist.playlist_name,
        avatar_url=playlist.playlist_image_url,
        is_owner=is_owner,
    )


@playlist_bp.route('/delete', methods=['DELETE'])
@login_required
def delete():
    user_playlist = PlaylistModel.find_by_user_id(session.get('user_id'))
    if not user_playlist:
        abort(404)

    user_playlist.delete_from_db()
    return url_for('me.my_page'), 200


@playlist_bp.route('<playlist_id>/change-name', methods=['PUT'])
@login_required
def change_display_name(playlist_id):
    playlist = PlaylistModel.find_by_id_or_404(playlist_id)

    if not playlist.owner_user_id == session.get('user_id'):
        abort(401)

    if request.form.get('new_name').strip() == '':
        return str('cannot be empty'), 400

    playlist.playlist_name = request.form.get('new_name')
    playlist.save_to_db()

    return str(playlist.playlist_name), 200


@playlist_bp.route('/import/', methods=['GET', 'POST'])
def import_playlist():
    # check if user is logged in
    if session.get('access_token') is None:
        return 'unauthorized', 401

    playlist_id = request.form.get('playlist_id')
    if playlist_id is None:
        return jsonify(message='no playlist id'), 400

    playlist_obj = PlaylistModel.find_by_id(playlist_id)
    if not playlist_obj:
        abort(404)

    uris_list = playlist_obj.get_uris_list(playlist_id=playlist_id)
    if uris_list is None:
        return jsonify(message='no items to add'), 400

    new_playlist_id = create_playlist(playlist_obj.playlist_name)

    if new_playlist_id is None:
        abort(500)

    add_tracks_to_playlist(track_uris=uris_list, playlist_id=new_playlist_id)

    # increase import_count
    playlist_obj.import_count += 1
    playlist_obj.save_to_db()

    return 'playlist created successfully', 201

"""
Users in this view can access their personal info
"""
from flask import Blueprint, render_template, request, abort, session, url_for
from app.auth import spotify
from app.utils import login_required
from app.errors import TokenExpired
from app.models import PlaylistModel

me_bp = Blueprint('me', __name__)


@me_bp.route('/me/')
@login_required
def my_page():
    me = spotify.get('me')

    if me.status == 401:
        raise TokenExpired(next_url=request.endpoint)

    if me.status != 200:
        abort(500)

    session['user_id'] = me.data.get('id')
    session['display_name'] = me.data.get('display_name')
    if len(me.data.get('images')) > 0:
        session['avatar_url'] = me.data['images'][0]['url']
    else:
        session['avatar_url'] = url_for('static', filename='images/spotify_icon.png', _external=True)

    user_playlist = PlaylistModel.find_by_user_id(me.data.get('id'))

    return render_template(
        'me.html',
        data=me.data,
        active='profile',
        avatar_url=session.get('avatar_url'),
        user_playlist=user_playlist,
    )

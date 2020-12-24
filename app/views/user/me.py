"""
Users in this view can access their personal info
"""
from flask import Blueprint, render_template, request, abort
from app.auth import spotify
from app.utils import login_required
from app.errors import TokenExpired

me_bp = Blueprint('me', __name__)


@me_bp.route('/me/')
@login_required
def my_page():
    me = spotify.get('me')

    if me.status == 401:
        raise TokenExpired(next_url=request.endpoint)

    if me.status != 200:
        abort(500)

    return render_template(
        'me.html',
        data=me.data,
        active='profile',
        avatar_url=me.data['images'][0]['url'],

    )

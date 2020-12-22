"""
Users in this view can access their personal info
"""
from flask import Blueprint, render_template, redirect, url_for, abort
from app.auth import spotify
from app.utils import login_required

me_bp = Blueprint('me', __name__)


@me_bp.route('/me/')
@login_required
def my_page():
    me = spotify.get('me')

    if me.status != 200:
        abort(500)

    return render_template(
        'me.html',
        data=me.data,
        active='profile',
        avatar_url=me.data['images'][0]['url'],

    )

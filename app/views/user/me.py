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
    if 'error' in me.data:
        if "The access token expired" in me.data.get('error').get('message'):
            return redirect(url_for('auth.auth_user'))
    if me.status != 200:
        abort(500)

    return render_template(
        'me.html',
        data=me.data,
        active='profile',
        avatar_url=me.data['images'][0]['url'],

    )

"""
Users in this view can access their personal info
"""
from flask import Blueprint, jsonify, redirect, url_for
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
    return jsonify(me.data)

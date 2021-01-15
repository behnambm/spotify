"""
This view is for landing_bp page
landing_bp page is the first page that user will see when opens the root URL
"""
from flask import render_template, Blueprint, request
from app.models import PlaylistModel

landing_bp = Blueprint('landing', __name__)


@landing_bp.route('/')
def landing_page():
    page = request.args.get('page', 1, type=int)
    playlists = PlaylistModel.query.order_by(PlaylistModel.created_at.desc()).paginate(
        page=page, per_page=8, error_out=False
    )

    return render_template(
        'home.html',
        playlists=playlists.items,
        pagination=playlists  # this is a pagination object
    )

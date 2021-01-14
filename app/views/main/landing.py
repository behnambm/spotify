"""
This view is for landing_bp page
landing_bp page is the first page that user will see when opens the root URL
"""
from flask import render_template, Blueprint
from app.models import PlaylistModel

landing_bp = Blueprint('landing', __name__)


@landing_bp.route('/')
@landing_bp.route('/home/')
@landing_bp.route('/index/')
def landing_page():
    return render_template(
        'home.html',
        playlists=PlaylistModel.query.all(),
    )

"""
This view is for landing_bp page
landing_bp page is the first page that user will see when opens the root URL
"""
from flask import render_template, Blueprint, session, redirect, url_for

landing_bp = Blueprint('landing', __name__)


@landing_bp.route('/')
@landing_bp.route('/home/')
@landing_bp.route('/index/')
def landing_page():
    if 'access_token' in session:
        return redirect(url_for('me.my_page'))
    return render_template('landing.html')

from flask import session, flash, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('access_token') is None:
            flash('You need to log-in first.', 'error')
            return redirect(url_for('landing.landing_page')), 401
        return f(*args, **kwargs)
    return wrapper


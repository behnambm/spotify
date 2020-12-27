from app import create_app
from os import getenv
from flask import session
from app.models import db

app = create_app()

db.init_app(app)
with app.app_context():
    db.create_all()


# to load variables(globally) inside jinja2 templates
@app.context_processor
def inject_data_to_template():
    logged_in = False
    if session.get('access_token') is not None:
        logged_in = True

    return dict(
        app_title=getenv('APP_TITLE'),
        logged_in=logged_in
    )

from app.models import db


class PlaylistModel(db.Model):
    __tablename__ = 'spotify_playlists'
    id = db.Column(db.String, primary_key=True)
    playlist_name = db.Column(db.String, nullable=False)
    import_count = db.Column(db.Integer, nullable=False, default=0)
    shared_by = db.Column(db.String, nullable=False)
    track_uris = db.Column(db.String)
    user_avatar_url = db.Column(db.String)



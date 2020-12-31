from flask_sqlalchemy import SQLAlchemy
from typing import Union
import time


db = SQLAlchemy()

association_table = db.Table('spotify_association',
    db.Column('playlist_id', db.Integer, db.ForeignKey('spotify_playlists.id')),
    db.Column('track_id', db.Integer, db.ForeignKey('spotify_tracks.id'))
)


class PlaylistModel(db.Model):
    __tablename__ = 'spotify_playlists'
    id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String, nullable=False)
    import_count = db.Column(db.Integer, nullable=False, default=0)
    owner_user_id = db.Column(db.String)
    created_at = db.Column(db.Float, default=time.time)
    tracks = db.relationship('TracksModel', secondary=association_table)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class TracksModel(db.Model):
    __tablename__ = 'spotify_tracks'
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String)
    artists_name = db.Column(db.String)
    album_name = db.Column(db.String)
    track_uri = db.Column(db.String, unique=True)
    explicit = db.Column(db.Boolean)
    track_duration = db.Column(db.String)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_uri(cls, uri: str) -> Union['TracksModel', None]:
        return cls.query.filter_by(track_uri=uri).first() or None

    @classmethod
    def check_and_save_to_db(cls, track: dict) -> None:
        if cls.find_by_uri(track.get('track_uri')) is None:
            new_row = cls(
                track_name=track.get('track_name'),
                artists_name=track.get('artists_name'),
                album_name=track.get('album_name'),
                track_uri=track.get('track_uri'),
                explicit=track.get('explicit'),
                track_duration=track.get('track_duration'),
            )
            new_row.save_to_db()

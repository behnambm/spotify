from marshmallow import Schema, fields


class PlaylistSchema(Schema):
    track_name = fields.Str(required=True)
    artists_name = fields.Str(required=True)
    album_name = fields.Str(required=True)
    track_uri = fields.Str(required=True)
    explicit = fields.Boolean(required=True)
    track_duration = fields.Str(required=True)

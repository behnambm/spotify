from marshmallow import Schema, fields


class PlaylistSchema(Schema):
    track_name = fields.Str(required=True)
    artists_name = fields.Str(required=True)
    album_name = fields.Str(required=True)
    track_id = fields.Str(required=True)
    is_explicit = fields.Boolean(required=True)
    track_duration = fields.Str(required=True)

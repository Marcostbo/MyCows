from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(required=True)
    public_id = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    date_joined = fields.DateTime(required=True)

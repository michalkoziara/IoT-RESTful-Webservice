from app.main.model.user import User

from marshmallow import fields
from marshmallow import Schema
from marshmallow import post_load


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    registered_on = fields.DateTime()
    admin = fields.Boolean()
    public_id = fields.String()
    username = fields.String()

    @post_load
    def deserialize_user(self, data, **kwargs):
        return User(**data)

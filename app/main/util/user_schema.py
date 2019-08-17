from marshmallow import Schema, fields, post_load
from ..model.user import User

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
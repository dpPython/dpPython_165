from marshmallow import Schema, fields


class UsersSchema(Schema):
    id = fields.UUID()
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password_hash = fields.Str(required=True)
    user_address = fields.Str()
    create_user_date = fields.DateTime()

    class Meta:
        fields = ('id', 'username', 'email', 'password_hash', 'user_address', 'create_user_date')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

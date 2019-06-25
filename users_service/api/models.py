from manage import db, ma, bcrypt
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text
import datetime
# from uuid import uuid4


class Users(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    # id = db.Column(db.Text, primary_key=True, unique=True, default=uuid4())
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    user_address = db.Column(db.String(200))
    create_user_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<User {}'.format(self.username)

    def set_password(self, password_hash):
        self.password_hash = bcrypt.generate_password_hash(password_hash)

    def check_password(self, password_hash):
        return bcrypt.check_password_hash(self.password_hash, password_hash)


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password_hash', 'user_address', 'create_user_date')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

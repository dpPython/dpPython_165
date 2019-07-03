from manage import db, bcrypt
from sqlalchemy.dialects.postgresql import UUID
import datetime
from uuid import uuid4


class Users(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_address = db.Column(db.String(200))
    create_user_date = db.Column(db.DateTime, default=datetime.datetime.utcnow().isoformat())

    def __repr__(self):
        return '<User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

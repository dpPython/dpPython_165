from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from .config import db


class Projects(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(), unique=False, nullable=True)
    contract_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    status = db.Column(db.String(), unique=False, nullable=False)
    rooms_data = db.relationship('Data')


class Data(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('projects.id'))
    field_1 = db.Column(db.Integer())
    field_2 = db.Column(db.Integer())
    field_3 = db.Column(db.Float())
    field_4 = db.Column(db.Integer())
    field_5 = db.Column(db.String(80))
    field_6 = db.Column(db.Float())
    field_7 = db.Column(db.Integer())
    field_8 = db.Column(db.Integer())
    field_9 = db.Column(db.Integer())
    field_10 = db.Column(db.String(80))
    field_11 = db.Column(db.Boolean())
    field_12 = db.Column(db.Integer())
    field_13 = db.Column(db.Float())
    field_14 = db.Column(db.Integer())
    field_15 = db.Column(db.Integer())
    field_16 = db.Column(db.Integer())
    field_17 = db.Column(db.String(80))
    field_18 = db.Column(db.Float())
    field_19 = db.Column(db.Integer())
    field_20 = db.Column(db.Integer())

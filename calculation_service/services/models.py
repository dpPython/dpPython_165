from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .config import db




class Calculation(db.Model):
    id = db.Column(UUID, primary_key=True, default=uuid4)
    project_id = db.Column(unique=True)
    # result = db.Column(db.Decimal, default=0)
    error_relation = db.relation('Errors')

class Errors(db.Model):
    id = db.Column(UUID, primary_key=True, default=uuid4)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    calculation_id = db.Column(UUID, db.ForeignKey('calculation.id'))

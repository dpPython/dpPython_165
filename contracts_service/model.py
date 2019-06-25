from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class Rule(db.Model):
    __tablename__ = 'rules'
    id = db.Column(db.Integer, primary_key=True)
    square = db.Column(db.Float, nullable=False)
    living_square = db.Column(db.Float, nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    toilets = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id', ondelete='CASCADE'), nullable=False)
    contract = db.relationship('Contract', backref=db.backref('rules', lazy='dynamic'))

    def __init__(self, contract_id, square, living_square, rooms, toilets):
        self.contract_id = contract_id
        self.square = square
        self.living_square = living_square
        self.rooms = rooms
        self.toilets = toilets


class Contract(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class ContractSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class RuleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    contract_id = fields.Integer(required=True)
    square = fields.Float(required=True)
    living_square = fields.Float(required=True)
    rooms = fields.Integer(required=True)
    toilets = fields.Integer(required=True)
    creation_date = fields.DateTime()

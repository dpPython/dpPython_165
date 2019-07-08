from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


db = SQLAlchemy()
ma = Marshmallow()


class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class Contract(db.Model, AddUpdateDelete):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    contract_name = db.Column(db.String(250), unique=True, nullable=False)
    information = db.Column(db.String(250))
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    rule_id = db.Column(UUID(as_uuid=True), db.ForeignKey('rule.id'), nullable=False)
    rule = db.relationship('Rule', backref=db.backref('contracts', lazy='dynamic' , order_by='Contract.contract_name'))

    def __init__(self, contract_name, information, rule):
        self.contract_name = contract_name
        self.information = information
        self.rule = rule


class Rule(db.Model, AddUpdateDelete):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(150), unique=True, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    f_operand = db.Column(db.String(250), nullable=False)
    s_operand = db.Column(db.String(250), nullable=False)
    operator = db.Column(db.String(2), nullable=False)
    coefficient = db.Column(db.String(250), nullable=False)

    def __init__(self, name, f_operand, s_operand, operator, coefficient):
        self.name = name
        self.f_operand = f_operand
        self.s_operand = s_operand
        self.operator = operator
        self.coefficient = coefficient


class RuleSchema(ma.Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor('api.ruleresource', id='<id>', _external=True)
    contracts = fields.Nested('ContractSchema', many=True, exclude=('rule',))
    creation_date = fields.DateTime()
    f_operand = fields.String(validate=validate.Length(1))
    s_operand = fields.String(validate=validate.Length(1))
    operator = fields.String(validate=validate.Length(1))
    coefficient = fields.String(validate=validate.Length(1))


class ContractSchema(ma.Schema):
    id = fields.UUID(dump_only=True)
    contract_name = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()
    rule = fields.Nested('RuleSchema', exclude=('contracts',))
    url = ma.URLFor('api.contractresource', id='<id>', _external=True)
    information = fields.String(validate=validate.Length(1))

    @pre_load
    def process_rule(self, data):
        rule = data.get('rule')
        if rule:
            if isinstance(rule, dict):
                rule_name = rule.get('name')
            else:
                rule_name = rule
            rule_dict = dict(name=rule_name)
        else:
            rule_dict = {}
        data['rule'] = rule_dict
        return data

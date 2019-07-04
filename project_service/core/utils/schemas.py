from marshmallow import Schema, fields, pprint


class ProjectSchema(Schema):
    id = fields.Str()
    status = fields.Str()
    name = fields.Str(required=True)
    contract_id = fields.UUID(required=True)


class DataNestedSchema(Schema):
    filed_1 = fields.Integer()
    filed_2 = fields.Integer()
    field_3 = fields.Float()
    filed_4 = fields.Integer()
    field_5 = fields.Str()
    field_6 = fields.Float()
    field_7 = fields.Integer()
    field_8 = fields.Integer()
    field_9 = fields.Integer()
    field_10 = fields.String()
    field_11 = fields.Bool()
    field_12 = fields.Integer()
    field_13 = fields.Float()
    field_14 = fields.Integer()
    field_15 = fields.Integer()
    field_16 = fields.Integer()
    field_17 = fields.Str()
    field_18 = fields.Float()
    field_19 = fields.Integer()
    field_20 = fields.Integer()


class DataSchema(Schema):
    data = fields.Nested(DataNestedSchema, many=True)



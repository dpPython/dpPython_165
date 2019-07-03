from marshmallow import Schema, fields, pprint


class ProjectSchema(Schema):
    status = fields.Str()
    name = fields.Str()
    contract_id = fields.UUID()


class PriceSchema(Schema):
    currency_value = fields.Float()
    currency = fields.Str()


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


if __name__ == '__main__':
    data = {
        'status': 'create_schema',
        'name': 'arthur',
        'contract_id': 'adsf'
    }

    nested_data = {
        'data': [
            {
                "address": "P.O. Box 664, 3059 Litora Road",
                "city": "Presteigne",
                "square": 237.0,
                "living_square": 161.0,
                "rooms": 3,
                "published_date": "2017-11-22T09:58:00+00:00",
                "price":
                    {
                        "currency_value": 14.83,
                        "currency": "USD"
                    },
                "toilets": 3
            },
            {
                "address": "fsdfasasdfasdf",
                "city": "asdfasfde",
                "square": 23.1,
                "living_square": 1.3,
                "rooms": 5,
                "published_date": "2017-11-22T09:58:00+00:00",
                "price":
                    {
                        "currency_value": 1.83,
                        "currency": "RU"
                    },
                "toilets": 0
            }
        ]
    }

    schema = DataSchema()
    result = schema.load(nested_data)
    pprint(result)

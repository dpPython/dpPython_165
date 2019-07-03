from marshmallow import Schema, fields, validates, ValidationError


class CsvFileUploadSchema(Schema):
    file = fields.Raw(required=True, missing=None)
    uuid = fields.UUID(required=True, missing=None)
    session = fields.UUID(required=True, missing=None)

    @validates('file')
    def validate_file(self, value):
        if value is None:
            raise ValidationError('Please provide a file')

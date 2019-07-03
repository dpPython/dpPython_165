from marshmallow import Schema, fields, validates, ValidationError, pre_load
import uuid


class CsvFileUploadSchema(Schema):
    file = fields.Raw(required=True, missing=None)
    uuid = fields.String(required=True, missing=None)
    session = fields.String(required=True, missing=None)

    @pre_load
    def parse(self, data):
        parsed_data = dict()
        form = data.form
        files = data.files
        parsed_data['file'] = files.get('file')
        parsed_data['uuid'] = form.get('project_id')
        parsed_data['session'] = form.get('session_id')
        return parsed_data

    @validates('file')
    def validate_file(self, value):
        if value.files.get('file') is None:
            raise ValidationError('Please provide a file')

    @validates('session')
    def validate_file(self, value):
        if not self._uuid_validate(value):
            raise ValidationError(f'{value} is not valid')

    @validates('uuid')
    def validate_file(self, value):
        if not self._uuid_validate(value):
            raise ValidationError(f'{value} is not valid')

    @staticmethod
    def _uuid_validate(uuid_string):
        return isinstance(uuid.UUID(uuid_string), uuid.UUID)

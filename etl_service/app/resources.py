from flask import jsonify, request, abort
from flask_restful import Resource
from flask_uploads import UploadSet

from .controllers import DataTransferCommunicator
from .schemes.upload_scheme import CsvFileUploadSchema
from .services.services_senders import SessionService

csv_uploader = UploadSet('CsvUploader')


class UploadCsv(Resource):
    sessions_service = SessionService()

    def post(self):
        filename, project_id, session_id = self._validate_request(request)
        self._validate_session(session_id)
        self.run_transfer(filename, "parser1", project_id)
        return jsonify(dict(result='success'))

    @staticmethod
    def run_transfer(filename, parser_name, project_uuid):
        process = DataTransferCommunicator(filename, parser_name, project_uuid)
        process.transfer_data.delay(process)

    def _validate_session(self, session_id):
        response = self.sessions_service.get(session_id)
        if response.status_code != 200:
            abort(300, {"message": "unauthorized access"})

    @staticmethod
    def _validate_request(request_):
        schema = CsvFileUploadSchema().load(request_.files)
        if schema.errors:
            abort(400, {'message': schema.errors["file"]})
        filename = csv_uploader.save(schema.data['file'])
        return csv_uploader.path(filename)

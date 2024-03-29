from flask import jsonify, request, abort
from flask_restful import Resource
from flask_uploads import UploadSet

from .celery_proj.tasks import transfer_data
from .schemes.upload_scheme import CsvFileUploadSchema
from .services.services_senders import SessionService

csv_uploader = UploadSet('CsvUploader')
CHUNK_SIZE = 50


class UploadCsv(Resource):
    sessions_service = SessionService()

    def post(self):
        filename, project_id, session_id = self._validate_request(request)
        # self._validate_session(session_id)
        transfer_data.delay(project_id, CHUNK_SIZE, filename,
                            "parser1")
        return jsonify(dict(result='success'))

    def _validate_session(self, session_id):
        response = self.sessions_service.get(session_id)
        if response.status_code != 200:
            abort(300, {"message": "unauthorized access"})

    @staticmethod
    def _validate_request(request_):
        schema = CsvFileUploadSchema().load(request_)
        if schema.errors:
            abort(400, {'message': schema.errors["file"]})
        filename = csv_uploader.save(schema.data['file'])
        return csv_uploader.path(filename), schema.data['uuid'], \
               schema.data['session']

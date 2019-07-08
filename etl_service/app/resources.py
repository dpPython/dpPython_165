from flask import jsonify, request, abort, g
from flask_restful import Resource
from flask_uploads import UploadSet

from .celery_proj.tasks import transfer_data
from .schemes.upload_scheme import CsvFileUploadSchema

csv_uploader = UploadSet('CsvUploader')
CHUNK_SIZE = 50


class UploadCsv(Resource):
    project_serice_url = "http://projects_service:6000/projects/{uuid}"

    def post(self):
        filename, project_id, session_id = self._validate_request(request)
        transfer_data.delay(self.project_serice_url.format(uuid=project_id),
                            CHUNK_SIZE, filename, "parser1")
        g.auth_cred = request.headers.get('Authorization')
        return jsonify(dict(result='success'))

    @staticmethod
    def _validate_request(request_):
        schema = CsvFileUploadSchema().load(request_)
        if schema.errors:
            abort(400, {'message': schema.errors["file"]})
        filename = csv_uploader.save(schema.data['file'])
        return csv_uploader.path(filename), schema.data['uuid'], \
               schema.data['session']

from csv import DictReader

from flask import jsonify, Response
from flask_restful import Resource

from .utils import (
    TransformType, RequestSender, save_filename, remove_file,
    post_parser
    )


class UploadCsv(Resource):

    sender = RequestSender()
    type_transformer = TransformType()

    def post(self):
        data = post_parser()
        file = data.get('file', False)
        if file:
            self.process_file(file)
            return jsonify(dict(result='success'))
        return Response(response=jsonify(dict(error="No file specified")),
                        status=400, mimetype='application/json')

    def process_file(self, file):
        uploaded_file = self._upload_file(file)
        try:
            self.form_request_data(uploaded_file)
        finally:
            remove_file(uploaded_file)

    def form_request_data(self, file):
        with open(file, 'r') as csv:
            self.sender.send_status('In progress')
            dict_file = DictReader(csv)
            self.process_data_file(dict_file)
            self.sender.send_status('Complete')

    def process_data_file(self, data_file, chunk=50):
        data_list = []
        for line in data_file:
            data_list.append(self._process_line(line))
            if len(data_list) == chunk or len(line) == 0:
                self.sender.send_chunk(data_list)
                data_list.clear()

    def _process_line(self, line):
        data = line
        return dict(
                address=data.get('address'), city=data.get('city'),
                square=self.type_transformer.transform_to_float(data.get(
                    'square')),
                living_square=self.type_transformer.transform_to_float(
                    data.get('living square')),
                price=self.type_transformer.transform_to_currencies(
                    data.get('price per sq m')),
                published_date=self.type_transformer.transform_to_date(
                    data.get('publish date')),
                rooms=self.type_transformer.transform_to_int(data.get(
                    'rooms')),
                toilets=self.type_transformer.transform_to_int(data.get(
                    'toilet rooms'))
                )

    @staticmethod
    def _upload_file(file):
        save_path = save_filename(file)
        file.save(save_path)
        return save_path

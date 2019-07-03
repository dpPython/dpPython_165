from csv import DictReader

from celery import chain, group

from .celery.app import celery_app
from .parsers.base_parser import FileParser, ACTIONS
from .services.services_senders import ProjectService


class DataTransferCommunicator:
    project_service = ProjectService()

    def __init__(self, upload_file, parser_name, project_uuid):
        self.file_processor = FileProcessor(upload_file, parser_name)
        self.project = project_uuid

    @celery_app.task
    def transfer_data(self):
        started = self.send_status.delay(self, self.project, "started")
        ended = self.send_status.delay(self, self.project, "finished")
        workflow = chain(started, self.chunk_group_register, ended)()
        result = workflow.get()
        return result

    @celery_app.task
    def send_status(self, uuid, status):
        response = self.project_service.put(uuid, status)
        return response

    def chunk_group_register(self, chunk_size=50):
        results = []
        for chunk in self._create_chunk(chunk_size):
            results.append(self._send_chunk.delay(self, self.project, chunk))
        return group(results)

    def _create_chunk(self, chunk_size):
        offset_csv = self.file_processor.csv_file()
        chunk = []
        for line in offset_csv:
            chunk.append(line)
            if len(chunk) == chunk_size:
                yield chunk
                chunk.clear()

    @celery_app.task
    def _send_chunk(self, uuid, chunk):
        return self.project_service.post(uuid, chunk)


class FileProcessor(FileParser):
    def __init__(self, file_to_upload, parser_name):
        self.file_to_upload = open(file_to_upload, 'r')
        self.csv = None
        FileParser.__init__(self, parser_name)

    def csv_file(self):
        offset = self.parser.get("offset")
        return self.dict_reader_offset(self.file_to_upload, offset)

    def process_line(self, line):
        result = dict()
        for column, value in self.parser.get("columns").items():
            result[column] = ACTIONS[value["action"]](line.get(value.get(
                'col')))
        return result

    @staticmethod
    def dict_reader_offset(file, offset):
        csv = DictReader(file)
        if offset:
            for i in range(offset):
                next(csv)
        return csv

from csv import DictReader

from .parsers.base_parser import FileParser, ACTIONS, TYPES


def create_chunk(upload_file, parser_name, chunk_size):
    file_processor = FileProcessor(upload_file, parser_name)
    offset_csv = file_processor.csv_file()
    chunk = []
    for line in offset_csv:
        chunk.append(line)
        if len(chunk) == chunk_size:
            yield chunk
            chunk.clear()


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
            result[column] = TYPES.get(value.get('type'))(ACTIONS[value[
                "action"]](line.get(value.get('col'))))
        return result

    @staticmethod
    def dict_reader_offset(file, offset):
        csv = DictReader(file)
        if offset:
            for i in range(offset):
                next(csv)
        return csv

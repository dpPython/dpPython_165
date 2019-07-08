from flask import jsonify
import requests

from .celery import celery
from ..controllers import create_chunk


def send_status(url_to_send, status):
    return requests.put(url_to_send, {'status': status})


def send_chunks(url_to_send, chunk_size, upload_file, parser_name):
    chunk_group = []
    for chunk in create_chunk(upload_file, parser_name, chunk_size):
        chunk_group.append(send_chunk(url_to_send, chunk))
    return chunk_group


def send_chunk(url_to_send, chunk):
    data_chunk = jsonify(chunk)
    return requests.post(url_to_send, {'data': data_chunk})


@celery.task
def transfer_data(url_to_send, chnk_size, upload_file, parser_name):
    send_status(url_to_send, status='started')
    send_chunks(url_to_send, chnk_size, upload_file, parser_name)
    send_status(url_to_send, 'uploaded')

    return None

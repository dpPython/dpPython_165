from .celery import celery
from celery import chain, group
from flask import current_app

from ..controllers import create_chunk

@celery.task
def send_status(uuid, status):
    return current_app.projects.put(uuid, status)


@celery.task
def send_chunks(uuid, chunk_size, upload_file, parser_name):
    chunk_group = []
    for chunk in create_chunk(upload_file, parser_name, chunk_size):
        chunk_group.append(send_chunk.delay(uuid, chunk))
    return group(chunk_group)


@celery.task
def send_chunk(uuid, chunk):
    return current_app.projects.post(uuid, chunk)


@celery.task
def transfer_data(project_id, chnk_size, upload_file,parser_name):
    started = send_status.s(project_id, "In progress")
    ended = send_status.s(project_id, "ended")
    chunk_group = send_chunks.delay(project_id, chnk_size,
                                    upload_file,
                                    parser_name)
    workflow = chain(started, chunk_group, ended)
    result = workflow.get()
    return None

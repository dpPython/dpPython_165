from celery import chain, group

from ..controllers import create_chunk
from ..services.services_senders import SessionService, ProjectService
from .celery import celery

sessions = SessionService()
projects = ProjectService()

@celery.task
def send_status(uuid, status):
    #return projects.put(uuid, status)
	pass


@celery.task
def send_chunks(uuid, chunk_size, upload_file, parser_name):
    chunk_group = []
    for chunk in create_chunk(upload_file, parser_name, chunk_size):
        chunk_group.append(send_chunk.delay(uuid, chunk))
    return chunk_group


@celery.task
def send_chunk(uuid, chunk):
    #return sessions.post(uuid, chunk)
	pass


@celery.task
def transfer_data(project_id, chnk_size, upload_file,parser_name):
    workflow = chain(send_status.si(project_id, "In progress"), group(send_chunks(project_id, chnk_size,
                                    upload_file,
                                    parser_name)), send_status.si(project_id, "ended"))()
    result = workflow.get()
    return None

from kombu import Queue, Exchange

CELERY_QUEUES = (
    Queue('for_status', Exchange("for_status"), routing_key='for_status'),
    Queue('data_transfer', Exchange("data_transfer"),
          routing_key='data_transfer'),
    Queue('for_chunk_sender', Exchange("for_chunk_sender"),
          routing_key='for_chunk_sender'),
    )

CELERY_ROUTES = {
    'transfer_data': {
        'queue': 'data_transfer', 'routing_key':
            'data_transfer'
        },
    '_send_chunk': {
        'queue': 'for_chunk_sender', 'routing_key':
            'for_chunk_sender'
        },
    'send_status': {'queue': 'for_status', 'routing_key': 'for_status'}
    }

import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
    )


class FlaskConfig:
    UPLOAD_FILES_DEST = os.path.join(BASE_DIR, 'uploads')
    UPLOADS_DEFAULT_DEST = os.path.join(BASE_DIR, 'uploads')
    UPLOAD_FILES_ALLOW = ['csv', ]
    FLASK_AUTH_SERVICE = 'http://session_service:7000/sessions/{uuid}'

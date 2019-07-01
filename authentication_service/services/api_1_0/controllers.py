from datetime import datetime
from uuid import uuid4
from flask import current_app
from marshmallow import Schema, fields

TTL = 900 # 15 min for session


class SessionIdSchema(Schema):
    sid = fields.UUID()


class SessionSchema(Schema):
    status = fields.Str()
    sid = fields.UUID()


class SessionDetails:

    def __init__(self, username, user_id, sid):
        self.sid = sid
        self.username = username
        self.user_id = user_id
        self.create_time = datetime.now()


class LoginController:

    def login(username, user_id):
        if user_id != 'not_found':
            redis_client = current_app.extensions['redis']
            sid = uuid4()
            session_details = SessionDetails(username=username, user_id=user_id, sid=sid)
            schema = SessionSchema()
            result = schema.dump(session_details)
            redis_client.set(str(sid), result, ex=TTL)
            return {'status': 'success', 'session_id': sid}
        return {'status': 'failed', 'session_id': None}


class SessionDetailsController:

    def get_details(sid):
        schema = SessionIdSchema()
        sid_ser = schema.load(sid)
        redis_client = current_app.extensions['redis']
        session_details = redis_client.get(str(sid_ser))
        if session_details:
            return {'status': 'logged in'}
        return {'status': 'failed', 'desc': 'session doesn\'t exists'}


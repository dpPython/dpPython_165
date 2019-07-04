from datetime import datetime
from uuid import uuid4
from flask import current_app
from marshmallow import Schema, fields

TTL = 900 # 15 min for session


class SessionSchemaPost(Schema):
    status = fields.Str()
    sid = fields.UUID()


class UserSchema(Schema):
    id = fields.UUID()
    username = fields.Str()
    email = fields.Str()
    password_hash = fields.Str()
    user_address = fields.Str()
    create_user_date = fields.DateTime()


class SessionDetails:

    def __init__(self, status, sid):
        self.status = status
        self.sid = sid


class LoginController:

    def login(username, user_id):
        schema_send = SessionSchemaPost()
        user_schema = UserSchema()
        user = user_schema.loads(user_id)
        if user_id != 'not_found':
            redis_client = current_app.extensions['redis']
            sid = uuid4()
            session_details_redis = username + ',' + str(user_id) + ',' + str(datetime.now())
            redis_client.set(str(sid), session_details_redis, ex=TTL)
            send_session_details = SessionDetails('success', sid)
            result_send = schema_send.dump(send_session_details)
            return result_send
        send_session_details = SessionDetails('failed', None)
        result_send = schema_send.dump(send_session_details)
        return result_send


class SessionDetailsController:

    def get_details(sid):
        redis_client = current_app.extensions['redis']
        session_details = redis_client.get(str(sid))
        if session_details:
            return {'status': 'logged in'}
        return {'status': 'failed', 'desc': 'session doesn\'t exists', 'sid': sid}


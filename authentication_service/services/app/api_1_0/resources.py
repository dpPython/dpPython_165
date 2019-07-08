'''
from datetime import datetime
from uuid import uuid4
from flask import jsonify, current_app
from flask_restful import Resource, fields
# from requests import Response

TTL = 54000  # 5 minutes of active session
session = {}


class Authenticate(Resource):

    def get(self, username):
        response = "{'user_id': '5, Vasya'}"
        if response:
            self.session_create(username)
            return jsonify({'username': username})

    def post(self, username, password):
        return jsonify({'username': username,
                        'password': password})

    @staticmethod
    def session_create(username):
        redis_client = current_app.extensions['redis']
        session['session_id'] = redis_client.set('session_id', str(uuid4()), TTL)
        session['username'] = redis_client.set('username', username)
        session['datetime'] = redis_client.set('datetime', str(datetime.now()))


class SessionDetails(Resource):
    def get(self):
        redis_client = current_app.extensions['redis']
        session_id = redis_client.get('session_id').decode()
        return jsonify({'session_id': f'{session_id}'})
'''

from flask import jsonify, session
from flask_restful import Resource


class Login(Resource):

    def get(self, username):
        response = "{'user_id': '5, Vasya'}"
        if response:
            session['username'] = username
            session['user_id'] = response
            return jsonify({'username': username})


class SessionDetails(Resource):

    def get(self):
        if session['logged_in']:
            return jsonify(session['sid'])

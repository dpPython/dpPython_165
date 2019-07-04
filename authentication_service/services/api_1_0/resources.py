from flask import request
from flask_restful import reqparse, Resource
from services.data_api import AccessToUsers
from .controllers import LoginController, SessionDetailsController


parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('sid', type=str)


class Login(Resource):

    def post(self):
        args = parser.parse_args()
        username = args['username']
        user_id =  AccessToUsers.get(username)
        return LoginController.login(username, user_id)


class SessionDetails(Resource):

    def get(self):
        args = parser.parse_args()
        sid = args['sid']
        return SessionDetailsController.get_details(sid)

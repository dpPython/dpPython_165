from flask import request
from flask_restful import reqparse, Resource
from .controllers import LoginController, SessionDetailsController


parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('sid', type=str)


class Login(Resource):

    service_users_url = "127.0.0.1:5001/user/%s"


    def post(self):
        args = parser.parse_args()
        username = args['username']
        user_id = '1' # request.get(self.service_users_url % args['username'])
        return LoginController.login(username, user_id)


class SessionDetails(Resource):

    def get(self):
        args = parser.parse_args()
        sid = args['sid']
        return SessionDetailsController.get_details(sid)

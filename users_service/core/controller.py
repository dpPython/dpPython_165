from flask import request, abort
from flask_restful import Resource
from core.utils.schema import users_schema, user_schema
from core.models import Users
from core.utils.session import session


class UsersPostGet(Resource):
    def get(self):
        all_users = Users.query.all()
        return {'Users': users_schema.dump(all_users).data}

    def post(self):
        data = request.get_json() or {}
        user = Users()
        result = user_schema.load(data)
        from_model_atribure(data, user, result)
        with session() as db:
            db.add(user)
        return {'status': 'ok'}


class UsersPutGet(Resource):
    def get(self, username):
        user = Users.query.filter_by(username=username).first_or_404()
        return {'User': user_schema.dump(user).data}

    def put(self, username):
        # auth = requests.get('auth/<{}>'.format(username))   # проверка авторизован польз. или нет
        # if auth.status_code == 500:
        # if auth['status'] == 'failed':
        #   return abort(500, 'User is not authorized')

        user = Users.query.filter_by(username=username).first_or_404()
        data = request.get_json() or {}
        from_model_atribure(data, user)
        session()
        return {'status': 'update_ok'}


def from_model_atribure(data, user, result=None):
    if result is not None and result.errors != {}:
        return abort(401, 'Incorrect data')
    for field in ['username', 'email', 'user_address']:
        if field in data:
            setattr(user, field, data[field])
    if 'password_hash' in data:
        user.set_password(data['password_hash'])

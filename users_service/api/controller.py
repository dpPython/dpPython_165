from flask import jsonify, url_for, request
from flask_restful import Resource

from api import errors
from manage import db
from api.models import Users, user_schema, users_schema


class UsersGetAll(Resource):
    def get(self):
        all_users = Users.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result.data)


class UsersGet(Resource):
    def get(self, username):
        user = Users.query.filter_by(username=username).first_or_404()
        return user_schema.jsonify(user)


class UsersPost(Resource):
    def post(self):
        data = request.get_json() or {}
        if 'username' not in data or 'email' not in data or 'password_hash' not in data:
            return errors.bad_request('must include username, email and password fields')
        if Users.query.filter_by(username=data['username']).first():
            return errors.bad_request('please use a different username')
        if Users.query.filter_by(email=data['email']).first():
            return errors.bad_request('please use a different email address')
        user = Users()
        for field in ['username', 'email', 'user_address']:
            if field in data:
                setattr(user, field, data[field])
        if 'password_hash' in data:
            user.set_password(data['password_hash'])
        db.session.add(user)
        db.session.commit()
        response = user_schema.jsonify(user)
        response.status_code = 201
        response.headers['Location'] = url_for('api.usersget', username=user.username)
        return response


class UsersPut(Resource):
    def put(self, username):
        user = Users.query.filter_by(username=username).first_or_404()
        data = request.get_json() or {}
        if 'username' in data and data['username'] != user.username and \
                Users.query.filter_by(username=data['username']).first():
            return errors.bad_request('please use a different username')
        if 'email' in data and data['email'] != user.email and \
                Users.query.filter_by(email=data['email']).first():
            return errors.bad_request('please use a different email address')
        for field in ['username', 'email', 'user_address']:
            if field in data:
                setattr(user, field, data[field])
        if 'password_hash' in data:
            user.set_password(data['password_hash'])
        db.session.commit()
        return user_schema.jsonify(user)

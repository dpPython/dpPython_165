from flask import jsonify, url_for, request
from api.models import Users, user_schema, users_schema
from api.manage import db
from api import errors, bp


@bp.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = Users.query.filter_by(username=username).first_or_404()
    return user_schema.jsonify(user)
# http GET http://localhost:5000/api/users/alice


@bp.route('/users', methods=['GET'])
def get_users():
    all_users = Users.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)
# http GET http://localhost:5000/api/users


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password_hash' not in data:
        return errors.bad_request('must include username, email and password fields')
    if Users.query.filter_by(username=data['username']).first():
        return errors.bad_request('please use a different username')
    if Users.query.filter_by(email=data['email']).first():
        return errors.bad_request('please use a different email address')
    user = Users()
    for field in ['username', 'email', 'address']:
        if field in data:
            setattr(user, field, data[field])
    if 'password_hash' in data:
        user.set_password(data['password_hash'])
    db.session.add(user)
    db.session.commit()
    response = user_schema.jsonify(user)
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', username=user.username)
    return response
# http POST http://localhost:5000/api/users username=alice password_hash=dog email=alice@example.com address=Pushkina,27


@bp.route('/users/<username>', methods=['PUT'])
def update_user(username):
    user = Users.query.filter_by(username=username).first_or_404()
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            Users.query.filter_by(username=data['username']).first():
        return errors.bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            Users.query.filter_by(email=data['email']).first():
        return errors.bad_request('please use a different email address')
    for field in ['username', 'email', 'address']:
        if field in data:
            setattr(user, field, data[field])
    if 'password_hash' in data:
        user.set_password(data['password_hash'])
    db.session.commit()
    return user_schema.jsonify(user)
# http PUT http://localhost:5000/api/users/alice email=kolya@example.com


@bp.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    user = Users.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    response = user_schema.jsonify(user)
    response.status_code = 201
    return response
# http DELETE http://localhost:5000/api/users/mem

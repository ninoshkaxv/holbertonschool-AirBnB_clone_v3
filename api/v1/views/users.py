#!/usr/bin/python3
"""create a new view of users object handles all defualt RESTful API"""


from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, request, jsonify


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def show_all_users():
    """request: GET - show all users objects

       request: POST - create new user object and return new object in json
    """
    if request.method == 'GET':
        list_users = []
        obj_users = storage.all(User)
        for key, value in obj_users.items():
            user_json = value.to_dict()
            list_users.append(user_json)
        return jsonify(list_users)

    if request.method == 'POST':
        body_request = request.get_json()
        if not body_request:
            abort(400, 'Not a JSON')
        if 'email' not in body_request.keys():
            abort(400, 'Missing email')
        if 'password' not in body_request.keys():
            abort(400, 'Missing password')
        new_user = User(**body_request)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def show_single_user(user_id=None):
    """request: GET - list one user object based on given user_id

       request: PUT - update user info and return updated object in json

       request: DELETE - delete an user based on given user_id
    """
    if user_id is None:
        abort(404)
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(obj_user.to_dict())
    if request.method == 'PUT':
        update_user = request.get_json()
        if not update_user:
            abort(400, 'Not a JSON')
        for key, value in update_user.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(obj_user, key, value)
        obj_user.save()
        return jsonify(obj_user.to_dict()), 200
    if request.method == 'DELETE':
        storage.delete(obj_user)
        storage.save()
        return jsonify({}), 200

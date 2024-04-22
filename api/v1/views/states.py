#!/usr/bin/python3
"""Create a new view of States objects handles all default RESTFil API"""


from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def show_all_states():
    """request: GET - list all the state objects

       request: POST - create a new state onject and return new object in json
    """
    if request.method == 'GET':
        list_states = []
        obj_states = storage.all(State)
        for key, value in obj_states.items():
            state_json = value.to_dict()
            list_states.append(state_json)
        return jsonify(list_states)

    if request.method == 'POST':
        body_request = request.get_json()
        if not body_request:
            abort(400, 'Not a JSON')
        if 'name' not in body_request.keys():
            abort(400, 'Missing name')
        new_state = State(**body_request)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def show_single_state(state_id=None):
    """request: GET - list one state object based on given state_id

       request: PUT - update state info and return updated object in json

       request: DELETE - delete a state based on given state_id
    """
    if state_id is None:
        abort(404)
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(obj_state.to_dict())
    if request.method == 'PUT':
        update_state = request.get_json()
        if not update_state:
            abort(400, 'Not a JSON')
        for key, value in update_state.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj_state, key, value)
        obj_state.save()
        return jsonify(obj_state.to_dict()), 200
    if request.method == 'DELETE':
        storage.delete(obj_state)
        storage.save()
        return jsonify({}), 200

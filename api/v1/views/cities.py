#!/usr/bin/python3
"""Create a new view of States objects handles all default RESTFil API"""


from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import abort, request, jsonify


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def show_cities_by_State(state_id=None):
    """request: GET - return all city objects in json of the given state_id

       request: POST - create new city in given state and return it in json"""
    if state_id is None:
        abort(404)
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)

    if request.method == 'GET':
        list_cities = []
        obj_cities = storage.all(City)
        for obj_city in obj_cities.values():
            if state_id == obj_city.state_id:
                list_cities.append(obj_city.to_dict())
        return jsonify(list_cities)

    if request.method == "POST":
        body_request = request.get_json()
        if not body_request:
            abort(400, 'Not a JSON')
        if 'name' not in body_request.keys():
            abort(400, 'Missing name')
        new_city = City(**body_request)
        new_city.state_id = state_id
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def show_city(city_id=None):
    """request: GET - return the city of given city_id in Json

       request: PUT - update the city object and return it in json

       request: DELETE - delete one city of given city_id and return empty dict
    """
    if city_id is None:
        abort(404)
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(obj_city.to_dict())
    if request.method == 'PUT':
        update_city = request.get_json()
        if not update_city:
            abort(400, 'Not a JSON')
        for key, value in update_city.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj_city, key, value)
        obj_city.save()
        return jsonify(obj_city.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(obj_city)
        storage.save()
        return jsonify({}), 200

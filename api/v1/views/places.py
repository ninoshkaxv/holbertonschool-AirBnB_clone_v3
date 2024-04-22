#!/usr/bin/python3
"""Create a new view of Place objects handles all default RESTFul API"""


from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def show_all_places(city_id=None):
    """request: GET - return all place objestc in json of given city_id

       request: POST - create new place in given city and return it in json
    """
    if city_id is None:
        abort(404)
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)

    if request.method == 'GET':
        list_places = []
        obj_places = storage.all(Place)
        for obj_place in obj_places.values():
            if city_id == obj_place.city_id:
                list_places.append(obj_place.to_dict())
        return jsonify(list_places)

    if request.method == 'POST':
        body_request = request.get_json()
        if not body_request:
            abort(400, 'Not a JSON')
        if 'user_id' not in body_request.keys():
            abort(400, 'Missing user_id')
        if 'name' not in body_request.keys():
            abort(400, 'Missing name')
        if storage.get(User, body_request['user_id']) is None:
            abort(404)
        new_place = Place(**body_request)
        new_place.city_id = city_id
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def show_place(place_id=None):
    """request: GET - return the place of given place_id in Json

       request: PUT - update the place object and return it in json

       request: DELETE - delete a place of given place_id and return empty dict
    """
    if place_id is None:
        abort(404)
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(obj_place.to_dict())
    if request.method == 'PUT':
        update_place = request.get_json()
        if not update_place:
            abort(400, 'Not a JSON')
        for key, value in update_place.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(obj_place, key, value)
        obj_place.save()
        return jsonify(obj_place.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(obj_place)
        storage.save()
        return jsonify({}), 200

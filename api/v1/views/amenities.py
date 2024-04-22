#!/usr/bin/python3
"""create a new view of amenities handles all default RESTful API"""


from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, request, jsonify


@app_views.route('amenities', strict_slashes=False, methods=['GET', 'POST'])
def show_all_amenities():
    """request: GET - show all amenities objects

       request: POST - create new amenity object and return new object in json
    """
    if request.method == 'GET':
        list_amenities = []
        obj_amenities = storage.all(Amenity)
        for key, value in obj_amenities.items():
            amenity_json = value.to_dict()
            list_amenities.append(amenity_json)
        return jsonify(list_amenities)

    if request.method == 'POST':
        body_request = request.get_json()
        if not body_request:
            abort(400, 'Not a JSON')
        if 'name' not in body_request.keys():
            abort(400, 'Missing name')
        new_amenity = Amenity(**body_request)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def show_single_amenity(amenity_id=None):
    """request: GET - list one amenity object based on given amenity_id

       request: PUT - update amenity info and return updated object in json

       request: DELETE - delete an amenity based on given amenity_id
    """
    if amenity_id is None:
        abort(404)
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(obj_amenity.to_dict())
    if request.method == 'PUT':
        update_amenity = request.get_json()
        if not update_amenity:
            abort(400, 'Not a JSON')
        for key, value in update_amenity.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj_amenity, key, value)
        obj_amenity.save()
        return jsonify(obj_amenity.to_dict()), 200
    if request.method == 'DELETE':
        storage.delete(obj_amenity)
        storage.save()
        return jsonify({}), 200

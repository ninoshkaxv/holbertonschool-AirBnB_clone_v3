#!/usr/bin/python3
"""Module for places view"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity

@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def retrieve_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    place_list = []
    for place in places:
        place_list.append(place.to_dict())
    return jsonify(place_list)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Return a Place object based on its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if data is None:
        abort(400, 'Not a JSON')
    if user is None:
        abort(404)
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')

    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches for places"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    places = storage.all(Place).values()
    if 'states' in data:
        places = [place for place in places if place.city.state_id in data['states']]
    if 'cities' in data:
        places = [place for place in places if place.city_id in data['cities']]
    if 'amenities' in data:
        places = [place for place in places if data['amenities'] <= set([amenity.id for amenity in place.amenities])]
    place_list = []
    for place in places:
        place_list.append(place.to_dict())
    return jsonify(place_list)

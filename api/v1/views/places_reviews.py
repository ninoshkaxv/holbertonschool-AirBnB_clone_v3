#!/usr/bin/python3
"""Create new view for Review object handle all default RESTFul API actions"""


from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def show_reviews(place_id=None):
    """request: GET - retrieve all reviews of one place

       request: POST - create new review for one place
    """
    if place_id is None:
        abort(404)
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)

    if request.method == 'GET':
        list_reviews = []
        obj_reviews = storage.all(Review)
        for obj_review in obj_reviews.values():
            if place_id == obj_review.place_id:
                list_reviews.append(obj_review.to_dict())
        return jsonify(list_reviews)

    if request.method == 'POST':
        body_request = request.get_json()
        if not body_request:
            abort(400, 'Not a JSON')
        if 'user_id' not in body_request.keys():
            abort(400, 'Missing user_id')
        if storage.get(User, body_request['user_id']) is None:
            abort(404)
        if 'text' not in body_request.keys():
            abort(400, 'Missing text')
        new_review = Review(**body_request)
        new_review.place_id = place_id
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def show_review(review_id=None):
    """request: GET - return the review of given review_id in Json

       request: PUT - update the review object and return it in json

       request: DELETE - delete review of given review_id & return empty dict
    """
    if review_id is None:
        abort(404)
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(obj_review.to_dict())
    if request.method == 'PUT':
        update_review = request.get_json()
        if not update_review:
            abort(400, 'Not a JSON')
        for key, value in update_review.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(obj_review, key, value)
        obj_review.save()
        return jsonify(obj_review.to_dict()), 200
    if request.method == 'DELETE':
        storage.delete(obj_review)
        storage.save()
        return ({}), 200

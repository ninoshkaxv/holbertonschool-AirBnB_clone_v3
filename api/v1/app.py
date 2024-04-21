#!/usr/bin/python3
"""Initialize the app module """
from flask import Flask, jsonify
from os import getenv

app = Flask(__name__)

from models import storage
from api.v1.views import app_views

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage():
    """Close the current SQLAlchemy Session"""
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error"""
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)

#!/usr/bin/python3
"""Defines the main Flask app for the API"""
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

# Creating the Flask app
app = Flask(__name__)

# Registering the blueprint
app.register_blueprint(app_views)

# CORS
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


# Status route
@app.teardown_appcontext
def close_storage(self):
    storage.close()


# Error handling
@app.errorhandler(404)
def handle_not_found_error(error):
    """Handles 404 errors by returning a JSON-formatted response"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":

    host = os.getenv("HBNB_API_HOST")
    port = os.getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"

    app.run(host=host, port=port, threaded=True)

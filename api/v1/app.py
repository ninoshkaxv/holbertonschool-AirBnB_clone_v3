#!/usr/bin/python3
"""the first endpoint to return API status"""
from flask import Flask, Blueprint, render_template, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
cors = CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_currentsession(exc):
    """remove current session"""
    storage.close()


@app.errorhandler(404)
def handler_404(e):
    """return json when page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)

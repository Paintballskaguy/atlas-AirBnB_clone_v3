#!/usr/bin/python3

"""
Main app module to start Flask for the API
"""


from http.client import HTTPException
from flask import Flask, jsonify, Blueprint
from api.v1.views.index import app_views
from models import storage

# Initialize Flask
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception=None):
    """Closes storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error=None):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    """Handles 400 Bad Request errors by returning a JSON response"""
    message = error.description if isinstance(error, HTTPException) else str(error)
    return jsonify({"error": message}), 400


if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)

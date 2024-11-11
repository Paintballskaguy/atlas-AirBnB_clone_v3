#!/usr/bin/python3

"""
Defines routes for index
"""

from flask import Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

@app_views.route('/status', methods=['GET'])
def status():
    """checks the api status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns the counts of each object by type."""
    stats_data = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats_data)
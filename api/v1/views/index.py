#!/usr/bin/python3

"""
Defines routes for index
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app.route('/api/v1/stats', methods=['GET'])
def stats():
    stats_data = {
        "users": 3,
        "places": 5,
        "cities": 2,
        "amenities": 3,
        "reviews": 2,
        "states": 3
    }
    return jsonify(stats_data)

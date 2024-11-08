#!/usr/bin/python3

"""
Defines routes for index
"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON status response"""
    return jsonify({"status": "OK"})

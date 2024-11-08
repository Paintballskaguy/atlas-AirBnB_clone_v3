#!/usr/bin/python3

"""
This module provides endpoints related to the API status.

It includes a route to check the status of the API.
"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def status():
    """GET /status
    Returns:
        JSON response with "status": "OK" to indicate API is running.
    """
    return jsonify({"status": "OK"})

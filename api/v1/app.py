#!/usr/bin/python3
"""
This module sets up and runs the Flask API for the AirBnB clone project.

It creates the Flask app, registers blueprints, and sets up teardown 
methods to manage the application's context.
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

# Initialize the Flask app
app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """Closes the database session."""
    storage.close()

if __name__ == "__main__":
    # Run the Flask app with specified or default host and port
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)

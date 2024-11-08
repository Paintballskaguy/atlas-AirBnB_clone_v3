#!/usr/bin/python3

"""
Main app module to start Flask for the API
"""

from flask import Flask
from models import storage
from api.v1.views import app_views

# Initialize Flask
app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """Closes storage on teardown"""
    storage.close()

if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)

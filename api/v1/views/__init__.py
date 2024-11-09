"""
Initializes the views Blueprint for the API
"""

from flask import Blueprint

from api.v1.views.cities import app as cities_app

# Define the Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views after defining app_views to avoid circular imports
from api.v1.views import index  # You can import other views this way

# Do not import states here directly; it will be handled later

"""
Initializes the views Blueprint for the API
"""

from flask import Blueprint
from api.v1.views.states import *

# Define the Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views after defining app_views to avoid circular imports
from api.v1.views.index import *
from api.v1.views import states
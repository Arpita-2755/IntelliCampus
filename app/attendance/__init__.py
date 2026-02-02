from flask import Blueprint

attendance = Blueprint("attendance", __name__)

from . import routes

from flask import Blueprint

bp = Blueprint("rent",  __name__)

from main.rent import views

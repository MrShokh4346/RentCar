from flask import Blueprint

bp = Blueprint("car",  __name__)

from main.car import views

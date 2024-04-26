from flask import Blueprint

categories_blueprint = Blueprint('categories_blueprint', __name__, url_prefix='')

from .presentation import routes

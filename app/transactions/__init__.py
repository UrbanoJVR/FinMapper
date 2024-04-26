from flask import Blueprint

transactions_blueprint = Blueprint('transactions_blueprint', __name__, url_prefix='')

from . import routes

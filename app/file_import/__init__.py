from flask import Blueprint

file_import_blueprint = Blueprint('file_import_blueprint', __name__, url_prefix='')

from . import routes

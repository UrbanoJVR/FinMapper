from flask import Flask
from flask_babel import Babel
from config import config


def register_blueprints(app):
    from .file_import import file_import_blueprint
    app.register_blueprint(file_import_blueprint)

    from .categories import categories_blueprint
    app.register_blueprint(categories_blueprint)


def get_locale():
    return 'es'


babel = Babel()


def create_app(config_name):
    app = Flask(__name__)

    babel.init_app(app, locale_selector=get_locale)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    register_blueprints(app)

    return app

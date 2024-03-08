from flask import Flask
from flask_babel import Babel
from config import config


def register_blueprints(app):
    from .file_import import file_import as file_import_blueprint
    app.register_blueprint(file_import_blueprint)


def get_locale():
    return 'es'


babel = Babel()


def create_app(config_name):
    print('I AM CREATING THE APP WITH ENV ' + config_name)
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    register_blueprints(app)  # Registra el blueprint aquí

    return app

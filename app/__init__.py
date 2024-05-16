import os

from flask import Flask
from flask_babel import Babel
from flask_migrate import Migrate

from app.common_routes import page_not_found
from config import config
from database import db


def register_blueprints(app):
    from app.src.categories import categories_blueprint
    app.register_blueprint(categories_blueprint)

    from app.src.transactions import transactions_blueprint
    app.register_blueprint(transactions_blueprint)

    app.errorhandler(404)(page_not_found)


def get_locale():
    return 'es'


babel = Babel()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    config_name = os.getenv('APP_CONFIG') or 'default'

    babel.init_app(app, locale_selector=get_locale)
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    config[config_name].init_app(app)
    register_blueprints(app)

    return app

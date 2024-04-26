import os

from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config


def register_blueprints(app):
    from app.src.categories import categories_blueprint
    app.register_blueprint(categories_blueprint)

    from app.src.transactions import transactions_blueprint
    app.register_blueprint(transactions_blueprint)


def get_locale():
    return 'es'


babel = Babel()
db = SQLAlchemy()
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

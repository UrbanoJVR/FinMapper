from flask import Flask
from flask_babel import Babel, format_datetime
from flask_migrate import Migrate

from app.common_routes import page_not_found
from config import config
from database import db


def register_blueprints(app):
    from transactions.presentation.crud_transaction_routes import transactions_crud_blueprint
    app.register_blueprint(transactions_crud_blueprint)

    from transactions.presentation.load_transactions_file_routes import transactions_file_blueprint
    app.register_blueprint(transactions_file_blueprint)

    from categories.presentation.routes import categories_blueprint
    app.register_blueprint(categories_blueprint)

    app.errorhandler(404)(page_not_found)


def get_locale():
    return 'es'


babel = Babel()
migrate = Migrate()


def create_app(config_name='default'):
    app = Flask(__name__)

    babel.init_app(app, locale_selector=get_locale)
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    config[config_name].init_app(app)
    register_blueprints(app)

    # Add format_datetime to Jinja2 environment globals
    app.jinja_env.globals['format_datetime'] = format_datetime

    return app

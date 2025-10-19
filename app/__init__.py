from flask import Flask
from flask_babel import Babel, format_datetime
from flask_migrate import Migrate, upgrade
from flask_session import Session

from app.common_routes import page_not_found
from app.src.shared.format_utils import format_currency_es
from config import config
from database import db


def register_blueprints(app):
    from app.src.presentation.routes.crud_transaction_routes import transactions_crud_blueprint
    app.register_blueprint(transactions_crud_blueprint)

    from app.src.presentation.routes.load_transactions_file_routes import transactions_file_blueprint
    app.register_blueprint(transactions_file_blueprint)

    from app.src.presentation.routes.category_routes import categories_blueprint
    app.register_blueprint(categories_blueprint)

    from app.src.presentation.routes.dashboard_routes import dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    app.errorhandler(404)(page_not_found)


def get_locale():
    return 'es'


babel = Babel()
migrate = Migrate()
session = Session()


def create_app(config_name='default'):
    app = Flask(__name__)

    babel.init_app(app, locale_selector=get_locale)
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)
    config[config_name].init_app(app)
    register_blueprints(app)

    # Add format_datetime to Jinja2 environment globals
    app.jinja_env.globals['format_datetime'] = format_datetime
    
    # Add custom filter for Spanish currency formatting using Flask-Babel
    app.jinja_env.filters['currency_es'] = format_currency_es

    # Auto-migrate database on startup
    with app.app_context():
        try:
            upgrade()
            print("Database migrations applied successfully")
        except Exception as e:
            print(f"Warning: Could not apply database migrations: {e}")
            # Continue anyway - the app should still work

    return app

import os

import pytest
from bs4 import BeautifulSoup
from flask.testing import FlaskClient
from flask_migrate import upgrade, Config

from app import create_app
from database import db


@pytest.fixture(scope='function')
def db_test_it():
    _delete_db_file()

    app = create_app('test-it')
    with app.app_context():
        config = Config()
        config.set_main_option('script_location', os.path.join(os.path.dirname(__file__), '../../migrations'))
        upgrade()
        connection = db.engine.connect()
        transaction = connection.begin()
        db.session.bind = connection
        yield db
        transaction.rollback()
        connection.close()

    _delete_db_file()


def _delete_db_file():
    db_file = 'data-test.sqlite'

    if os.path.exists(db_file):
        os.remove(db_file)


@pytest.fixture(scope='function')
def client() -> FlaskClient:
    app = create_app('test')
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()

@pytest.fixture
def flask_app():
    app = create_app('test')
    app.secret_key = "test_secret_key"
    return app

def assert_flash_message_success_is_present(html_data, expected_message):
    html = BeautifulSoup(html_data, 'html.parser')
    flash_messages = html.find_all(class_='alert-success')
    assert any(expected_message in message.text for message in flash_messages), (
        f"Expected flash message '{expected_message}' not found."
    )

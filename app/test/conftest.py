import pytest
from bs4 import BeautifulSoup
from flask.testing import FlaskClient

from app import create_app
from database import db


@pytest.fixture(scope='function')
def client() -> FlaskClient:
    app = create_app('test')
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()

def assert_flash_message_success_is_present(html_data, expected_message):
    html = BeautifulSoup(html_data, 'html.parser')
    flash_messages = html.find_all(class_='alert-success')
    assert any(expected_message in message.text for message in flash_messages), (
        f"Expected flash message '{expected_message}' not found."
    )
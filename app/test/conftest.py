import pytest
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

import os
import sys

import pytest

from app import create_app
from database import db

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture(scope='session')
def client():
    app = create_app('test')
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()

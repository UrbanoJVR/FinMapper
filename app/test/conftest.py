import pytest

from app import create_app


@pytest.fixture(scope='module')
def client():
    yield create_app('test').test_client()


# @pytest.fixture(scope="module")
# def db_session():
#     Base.metadata.create_all(engine)
#     session = Session()
#     yield session
#     session.rollback()
#     session.close()

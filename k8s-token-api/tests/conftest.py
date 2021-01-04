
import pytest

from test_helper import create_random_database, delete_database


@pytest.fixture
def test_db(scope="function"):
    db, name = create_random_database()
    yield db
    delete_database(name)

import pytest

from estadosseguro import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret"})
    with app.test_client() as test_client:
        yield test_client

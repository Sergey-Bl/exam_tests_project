import pytest


@pytest.fixture(scope="module")
def user_credentials():
    return {
        "email": "rubetta5064@awgarstone.com",
        "password": "b3719ec9"
    }

import pytest


@pytest.fixture(scope="module")
def user_credentials():
    return {
        "email": "rubetta5064@awgarstone.com",
        "password": "b3719ec9"
    }


@pytest.fixture(scope="module")
def default_header_json_value():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json;version=1.1"
    }

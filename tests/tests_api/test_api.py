import pytest
import requests
from datetime import datetime
import data
from helpers.base_help_api import HelperApiTests


@pytest.mark.api("test_api_1")
def test_main_request():
    expected_url = f'{data.urls.DOMEN}'
    r_get = requests.get(expected_url)
    assert r_get.status_code == 200
    assert r_get.headers.get("content-type") == "text/html; charset=utf-8"
    assert r_get.headers.get("cache-control") == "no-cache"


@pytest.mark.api("test_api_2")
def test_main_request_negative():
    expected_url = f'{data.urls.DOMEN}+testest'
    r_get = requests.get(expected_url)
    assert r_get.status_code == 404


@pytest.mark.api("test_api_3")
def test_current_date_request():
    expected_url = f'{data.urls.DOMEN}'
    r_get = requests.get(expected_url)
    helper_api_tests = HelperApiTests()
    assert helper_api_tests.is_time_close(datetime.utcnow().strftime('%a, %d %b %Y %H:%M'), r_get.headers.get("date"),
                                          60)

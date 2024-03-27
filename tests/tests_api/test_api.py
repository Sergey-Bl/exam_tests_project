import json
import allure
import pytest
from datetime import datetime
import data
from helpers.base_help_api import HelperApiTests

session = HelperApiTests.create_unverified_session()


@allure.title("Тест-001: Смоук риквест проверки работы рестов")
@pytest.mark.api()
def test_main_request():
    expected_url = f'{data.urls.DOMEN}'
    r_get = session.get(expected_url)
    HelperApiTests.assert_status_code_2xx(r_get)
    assert r_get.headers.get("content-type") == "text/html; charset=utf-8"
    assert r_get.headers.get("cache-control") == "no-cache"


@allure.title("Тест-002: Проверка отдачи несуществующей урлы и ошибки 404")
@pytest.mark.api()
def test_main_request_negative():
    expected_url = f'{data.urls.DOMEN}+testest'
    r_get = session.get(expected_url)
    HelperApiTests.assert_status_code_4xx(r_get)


@allure.title("Тест-003: Проверка что хидер отдает верные данные/время")
@pytest.mark.api()
def test_current_date_request():
    expected_url = f'{data.urls.DOMEN}'
    r_get = session.get(expected_url)
    helper_api_tests = HelperApiTests()
    assert helper_api_tests.is_time_close(datetime.utcnow().strftime('%a, %d %b %Y %H:%M'), r_get.headers.get("date"),
                                          60)
    HelperApiTests.assert_status_code_2xx(r_get)


@allure.title("Тест-004: Проверка доступности урлы специальных предложений")
@pytest.mark.api()
def test_sp_request():
    expected_url = f'{data.urls.URL_SP_OFFERS}'
    r_get = session.get(expected_url)
    HelperApiTests.assert_status_code_2xx(r_get)
    assert r_get.headers.get("content-type") == "text/html; charset=utf-8"


@allure.title("Тест-005: Проверка доступности урлы корзины")
@pytest.mark.api()
def test_basket_request():
    expected_url = f'{data.urls.URL_BASKET}'
    r_get = session.get(expected_url)
    HelperApiTests.assert_status_code_2xx(r_get)
    assert r_get.headers.get("content-type") == "text/html; charset=utf-8"


@allure.title("Тест-006: Проверка доступности урлы сервисов")
@pytest.mark.api()
def test_services_request():
    expected_url = f'{data.urls.URL_SERVICES}'
    r_get = session.get(expected_url)
    HelperApiTests.assert_status_code_2xx(r_get)
    assert r_get.headers.get("content-type") == "text/html; charset=UTF-8"


@allure.title("Тест-006: Проверка доступности урлы компании")
@pytest.mark.api()
def test_about_request():
    expected_url = f'{data.urls.URL_ABOUT_COMPANY_PAGE}'
    r_get = session.get(expected_url)
    HelperApiTests.assert_status_code_2xx(r_get)
    assert r_get.headers.get("content-type") == "text/html; charset=UTF-8"


@allure.title("Тест-007: Авторизация пользователя")
@pytest.mark.api()
def test_user_login(user_credentials):
    payload = {
        "User": user_credentials
    }
    response = session.post(
        url=data.urls.URL_LOGIN,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json;version=1.1",
        },
        data=json.dumps(payload),
    )
    assert response.headers.get('x-gate-user-id') == '14372444'


@allure.title("Тест-008: Проверка операции выхода из системы")
@pytest.mark.api()
def test_user_logout(user_credentials):
    payload = {
        "User": user_credentials

    }
    response = session.post(
        url=data.urls.URL_LOGIN,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json;version=1.1",
        },
        data=json.dumps(payload),
    )
    assert response.headers.get('x-gate-user-id') == '14372444'

    response = session.post(
        url=data.urls.URL_LOGOUT,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json;version=1.1",
        },
        data=json.dumps({"route": "logout", "parameters": {}})
    )
    assert response.headers.get('x-gate-user-id') != '14372444'

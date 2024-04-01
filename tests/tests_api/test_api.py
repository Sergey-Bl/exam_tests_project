import json
from datetime import datetime, timezone

import requests
import pytest
import allure

from data import urls
from helpers.base_help_api import HelperApiTests
from tests.tests_api.conftest import logger

session = HelperApiTests.create_unverified_session()


@allure.title("Тест-001: Смоук риквест проверки работы рестов")
@pytest.mark.api_smoke()
def test_main_request():
    expected_url = f'{urls.DOMEN}'
    r_get = session.get(expected_url)
    HelperApiTests.assert_status_code_2xx(r_get)
    assert r_get.headers.get("content-type") == "text/html; charset=utf-8"
    assert r_get.headers.get("cache-control") == "no-cache"


@allure.title("Тест-002: Проверка отдачи несуществующей урлы и ошибки 404")
@pytest.mark.api_smoke()
def test_main_request_negative():
    expected_url = f'{urls.DOMEN}+testest'
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        try:
            r_get = session.get(expected_url)
            HelperApiTests.assert_status_code_4xx(r_get)
            assert r_get.headers.get("content-type") == "text/html; charset=UTF-8"
            break
        except requests.exceptions.RequestException:
            attempts += 1
            if attempts == max_attempts:
                raise


@allure.title("Тест-003: Проверка что хидер отдает верные данные/время")
@pytest.mark.api_smoke()
def test_current_date_request():
    expected_url = f'{urls.DOMEN}'
    r_get = session.get(expected_url)
    helper_api_tests = HelperApiTests()
    assert helper_api_tests.is_time_close(datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M'),
                                          r_get.headers.get("date"),
                                          60)
    HelperApiTests.assert_status_code_2xx(r_get)


@allure.title("Тест-004: Проверка доступности урлы специальных предложений")
@pytest.mark.api_smoke()
def test_sp_request():
    expected_url = f'{urls.URL_SP_OFFERS}'
    r_get = session.get(expected_url)
    HelperApiTests.assert_status_code_2xx(r_get)
    assert r_get.headers.get("content-type") == "text/html; charset=utf-8"


@allure.title("Тест-005: Проверка доступности урлы корзины")
@pytest.mark.api_smoke()
def test_basket_request():
    expected_url = f'{urls.URL_BASKET}'
    r_get = session.get(expected_url)
    HelperApiTests.assert_status_code_2xx(r_get)
    assert r_get.headers.get("content-type") == "text/html; charset=utf-8"


@allure.title("Тест-006: Проверка доступности урлы компании")
@pytest.mark.api_smoke()
def test_about_request():
    expected_url = f'{urls.URL_ABOUT_COMPANY_PAGE}'
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        try:
            r_get = session.get(expected_url)
            HelperApiTests.assert_status_code_2xx(r_get)
            assert r_get.headers.get("content-type") == "text/html; charset=UTF-8"
            break
        except requests.exceptions.RequestException:
            attempts += 1
            if attempts == max_attempts:
                raise


@allure.title("Тест-006: Проверка доступности урлы компании")
@pytest.mark.api_smoke()
def test_about_request():
    expected_url = f'{urls.URL_ABOUT_COMPANY_PAGE}'
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        try:
            r_get = session.get(expected_url)
            HelperApiTests.assert_status_code_2xx(r_get)
            assert r_get.headers.get("content-type") == "text/html; charset=UTF-8"
            break
        except requests.exceptions.RequestException:
            attempts += 1
            if attempts == max_attempts:
                raise


@pytest.mark.parametrize("user_credentials", [
    {"email": "rubetta5064@awgarstone.com", "password": "b3719ec9"},
])
@pytest.mark.api_user()
def test_user_login(user_credentials, default_header_json_value):
    login_payload = {
        "User": user_credentials
    }
    attempts = 0
    max_attempts = 20
    while attempts < max_attempts:
        try:
            login_response = session.post(
                url=urls.URL_LOGIN,
                headers=default_header_json_value,
                data=json.dumps(login_payload),
            )
            login_response.raise_for_status()
            user_id = login_response.headers.get('x-gate-user-id')
            assert user_id is not None, "Не удалось получить x-gate-user-id после авторизации"

        except requests.exceptions.RequestException as e:
            attempts += 1
            print(f"Попытка {attempts}/{max_attempts} не удалась: {e}")
            if attempts == max_attempts:
                logger.error(f"Тест не прошел, ссл не пускает")
                raise AssertionError(f"Тест не удался после {max_attempts} попыток")
            break


@pytest.mark.parametrize("user_credentials", [
    ({"email": "rubetta5064@awgarstone.com", "password": "b3719ec9"}),
])
@pytest.mark.api_user()
def test_user_logout(user_credentials, default_header_json_value):
    login_payload = {
        "User": user_credentials
    }
    attempts = 0
    max_attempts = 20
    while attempts < max_attempts:
        try:
            login_response = session.post(
                url=urls.URL_LOGIN,
                headers=default_header_json_value,
                data=json.dumps(login_payload),
            )
            login_response.raise_for_status()
            user_id = login_response.headers.get('x-gate-user-id')
            assert user_id is not None, "Не удалось получить x-gate-user-id после авторизации"

            logout_response = session.post(
                url=urls.URL_LOGOUT,
                headers=default_header_json_value,
                data=json.dumps({"route": "logout", "parameters": {}})
            )
            logout_response.raise_for_status()

            assert logout_response.headers.get(
                'x-gate-user-id') is None, "x-gate-user-id должен быть None после выхода из системы"
            break
        except requests.exceptions.RequestException as e:
            attempts += 1
            print(f"Попытка {attempts}/{max_attempts} не удалась: {e}")
            if attempts == max_attempts:
                raise AssertionError(f"Тест не удался после {max_attempts} попыток")


@allure.title("Тест-009: Ревью форма")
@pytest.mark.api_opinion()
def test_review_form(get_form_test_opinion):
    response = get_form_test_opinion

    attempts = 0
    max_attempts = 30
    while attempts < max_attempts:
        try:
            HelperApiTests.assert_status_code_2xx(response)
            assert 'id="form-add-review"' in response.text
            assert 'name="data[Review][reviewer_name]"' in response.text
            assert 'name="data[Review][reviewer_phone]"' in response.text
            assert 'name="data[Review][review_text]"' in response.text
            assert 'type="submit"' in response.text
            assert 'id="agreement"' in response.text
            break
        except requests.exceptions.RequestException:
            attempts += 1
            if attempts == max_attempts:
                raise


@allure.title("Тест-010: Вход с невалидными данными")
@pytest.mark.api_user()
def test_user_fail_login(default_header_json_value):
    payload = {"User": {
        "email": "rubetta506",
        "password": "b371asd9ec9"
    }}
    url = urls.URL_LOGIN
    headers = default_header_json_value
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        try:
            response = session.post(url, headers=headers, data=json.dumps(payload))
            HelperApiTests.assert_status_code_2xx(response)
            assert response.headers.get('x-gate-user-id') == ''
            break
        except requests.exceptions.RequestException:
            attempts += 1
            if attempts == max_attempts:
                raise


@allure.title("Тест-011: Попытка доступа с изменённым x-gate-user-id после авторизации")
@pytest.mark.api_security()
@pytest.mark.skip(reason="21 век банит за этот кейс")
def test_user_access_with_modified_userid(user_credentials, default_header_json_value):
    payload = {"User": user_credentials}
    login_url = urls.URL_LOGIN
    protected_url = urls.URL_LOGIN
    headers = default_header_json_value

    login_response = session.post(login_url, headers=headers, data=json.dumps(payload))
    assert login_response.headers.get('x-gate-user-id') == '14372444', "UserID не соответствует ожидаемому"
    modified_user_id = "12345678"
    modified_headers = {**headers, 'x-gate-user-id': modified_user_id}

    protected_response = session.put(protected_url, headers=modified_headers)

    HelperApiTests.assert_status_code_4xx(protected_response)


@allure.title("Тест-012: Вход с невалидными данными")
@pytest.mark.api_user()
def test_user_fail_incorrect_value(default_header_json_value):
    payload = {"User": {
        "email": "--/**&^%$kjasnd%^&",
        "password": "--/**&asdagh^%$%^&"
    }}
    url = urls.URL_LOGIN
    headers = default_header_json_value
    attempts = 0
    max_attempts = 50
    expected_error = "Введите email"

    while attempts < max_attempts:
        try:
            response = session.post(url, headers=headers, data=json.dumps(payload))
            response_data = response.json()
            HelperApiTests.assert_status_code_2xx(response)
            assert response_data.get(
                'error') == expected_error
            break
        except requests.exceptions.RequestException:
            attempts += 1
            if attempts == max_attempts:
                raise


@pytest.mark.parametrize("email,password,expected_error", [
    ("rubetta5064@awgarstone.com", "--/**&^%$%^&", "Введите email")])
@allure.title("Тест-013: Вход с невалидным паролем")
@pytest.mark.api_user()
def test_user_fail_login_sql_inq(email, password, expected_error, default_header_json_value):
    payload = {
        "User": {
            "email": email,
            "password": password
        }
    }
    url = urls.URL_LOGIN
    headers = default_header_json_value
    attempts = 0
    max_attempts = 50

    while attempts < max_attempts:
        try:
            response = session.post(url, headers=headers, data=json.dumps(payload))
            response_data = response.json()
            HelperApiTests.assert_status_code_2xx(response)
            assert response_data.get('error') == expected_error

            break
        except requests.exceptions.RequestException:
            attempts += 1
            if attempts == max_attempts:
                raise


@pytest.mark.parametrize("email", [
    "test2@gmail.com"])
@allure.title('Тест-014 Ошибка при обращении к апи без сертификата')
@pytest.mark.api_user()
def test_reset_password_local_ssl(email, default_header_json_value):
    headers = default_header_json_value
    url = urls.RESET_PASSWORD_URL
    response = session.post(url, headers=headers, data=json.dumps(email))
    HelperApiTests.assert_status_code_5xx(response)


@pytest.mark.parametrize("city, city_id", [
    ("г. Брест", "2458"),
])
@allure.title('Тест-015 получение инфы по доствакам')
@pytest.mark.api_delivery()
def test_delivery_info_response(city, city_id, default_header_json_value):
    attempts = 0
    max_attempts = 50
    params = {
        "region[city]": city,
        "region[type]": "г",
        "region[region]": "",
        "region[distance]": "0",
        "region[city_id]": city_id,
        "region[village_council]": "",
        "item": "null",
    }
    try:
        response = session.get(
            url=urls.DELIVERY_INFO_URL,
            params=params,
            headers=default_header_json_value
        )

        assert response.status_code == 200, f"Ожидался статус код 200, получен {response.status_code}"

        value_delivery = response.json()
        print(value_delivery)
        assert value_delivery['city_id'] == city_id
        expected_city_name = city.split(" ")[-1]
        assert value_delivery['name_object'] == expected_city_name
        assert 'delivery_group' in value_delivery
    except requests.exceptions.RequestException:
        attempts += 1
        if attempts == max_attempts:
            raise

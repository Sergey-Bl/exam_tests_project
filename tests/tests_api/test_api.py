import json, allure, pytest, requests
from datetime import datetime, timezone
from data import urls
from helpers.base_help_api import HelperApiTests

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
    r_get = session.get(expected_url)
    HelperApiTests.assert_status_code_4xx(r_get)


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


@allure.title("Тест-007: Авторизация пользователя")
@pytest.mark.api_user()
def test_user_login(user_credentials, default_header_json_value):
    payload = {"User": user_credentials}
    url = urls.URL_LOGIN
    headers = default_header_json_value

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            response = session.post(url, headers=headers, data=json.dumps(payload))

            assert response.headers.get('x-gate-user-id') == '14372444', "UserID не соответствует ожидаемому"
            break
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError) as e:
            print(f"Попытка {attempt} не удалась: {e}")
            if attempt == max_attempts:
                raise


@allure.title("Тест-008: Проверка операции выхода из системы")
@pytest.mark.api_user()
def test_user_logout(user_credentials, default_header_json_value):
    payload = {
        "User": user_credentials
    }
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        try:
            response = session.post(
                url=urls.URL_LOGIN,
                headers=default_header_json_value,
                data=json.dumps(payload),
            )
            assert response.headers.get('x-gate-user-id') == '14372444'

            response = session.post(
                url=urls.URL_LOGOUT,
                headers=default_header_json_value,
                data=json.dumps({"route": "logout", "parameters": {}})
            )
            assert response.headers.get('x-gate-user-id') != '14372444'
            break
        except requests.exceptions.ProxyError:
            attempts += 1
            if attempts == max_attempts:
                raise


@allure.title("Тест-009: Проверка операции выхода из системы")
@pytest.mark.api_opinion()
def test_review_form(session, get_form_test_opinion):
    response = get_form_test_opinion

    attempts = 0
    max_attempts = 5
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

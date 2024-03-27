from helpers.__init__ import datetime, requests


class HelperApiTests:
    @staticmethod
    def is_time_close(expected, actual, delta_seconds=60):
        expected_time = datetime.strptime(expected, '%a, %d %b %Y %H:%M')
        actual_time = datetime.strptime(actual, '%a, %d %b %Y %H:%M:%S GMT')
        return abs((expected_time - actual_time).total_seconds()) <= delta_seconds

    @staticmethod
    def create_unverified_session():
        session = requests.Session()
        session.verify = False
        return session

    # statuses checks
    def assert_status_code_1xx(response):
        assert 100 <= response.status_code < 200, f"Ожидался код из диапазона 100-199, получен: {response.status_code}"

    def assert_status_code_2xx(response):
        assert 200 <= response.status_code < 300, f"Ожидался код из диапазона 200-299, получен: {response.status_code}"

    def assert_status_code_3xx(response):
        assert 300 <= response.status_code < 400, f"Ожидался код из диапазона 300-399, получен: {response.status_code}"

    def assert_status_code_4xx(response):
        assert 400 <= response.status_code < 500, f"Ожидался код из диапазона 400-499, получен: {response.status_code}"

    def assert_status_code_5xx(response):
        assert 500 <= response.status_code < 600, f"Ожидался код из диапазона 500-599, получен: {response.status_code}"

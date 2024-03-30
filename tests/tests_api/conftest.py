import logging
import os
import shutil
from logging.handlers import RotatingFileHandler

import pytest
import requests

import data

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

log_file_path = 'logger/test_results_api.log'
log_dir = os.path.dirname(log_file_path)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024 * 5, backupCount=2)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@pytest.fixture(scope="module")
def user_credentials():
    return {
        "email": "rubetta5064@awgarstone.com",
        "password": "b3719ec9"
    }


@pytest.fixture(scope="module")
def get_form_test_opinion(session, default_header_json_value):
    url = data.urls.URL_OPINION_REST
    params = {
        "form": "Review",
        "item": "393764",
    }
    response = session.get(url, params=params, headers=default_header_json_value, verify=False)
    return response


@pytest.fixture(scope="module")
def default_header_json_value():
    return {
        "Host": "www.21vek.by",
        "Content-Type": "application/json",
        "Accept": "application/json;version=1.1"
    }


@pytest.fixture(scope="session")
def session():
    session = requests.Session()
    session.headers.update({'User-Agent': 'My User Agent 1.0'})
    return session


@pytest.fixture(autouse=True)
def test_logger(request):
    logger.info(f"Начало теста: {request.node.nodeid}")
    yield
    if hasattr(request.node, "rep_call"):
        if request.node.rep_call.passed:
            logger.info(f"Тест успешно пройден: {request.node.nodeid}")
        elif request.node.rep_call.failed:
            logger.error(f"Тест провален: {request.node.nodeid}")
        elif request.node.rep_call.skipped:
            logger.warning(f"Тест пропущен: {request.node.nodeid}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if item.rep_call.longrepr:
                msg = item.rep_call.longreprtext
            else:
                msg = item.rep_call.longrepr
            logger.error(f"Ошибка в тесте {item.nodeid}: {msg}")
        except AttributeError:
            logger.error(f"Ошибка в тесте {item.nodeid}, но подробности недоступны.")
    elif rep.when == "call":
        item.rep_call = rep


def pytest_sessionstart(session):
    allure_logs_dir = "allure_logs"
    if os.path.exists(allure_logs_dir):
        shutil.rmtree(allure_logs_dir)
    os.makedirs(allure_logs_dir, exist_ok=True)

    if os.path.exists(log_file_path):
        open(log_file_path, 'w').close()
        

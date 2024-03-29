from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import pages
from logging.handlers import RotatingFileHandler
import pytest
import logging
import os
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

log_file_path = 'logger/test_results_ui.log'

log_dir = os.path.dirname(log_file_path)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024 * 5, backupCount=2)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def create_driver_chrome(headless):
    chrome_options = webdriver.ChromeOptions()
    if headless == 'yes':
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver


def create_driver_firefox(headless):
    firefox_options = webdriver.FirefoxOptions()
    if headless == 'yes':
        firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
    return driver


@pytest.fixture(autouse=True)
def driver(request):
    headless = request.config.getoption('--headless')
    browser_type = request.config.getoption('--browser')

    if browser_type == 'chrome':
        driver = create_driver_chrome(headless)
    elif browser_type == 'firefox':
        driver = create_driver_firefox(headless)
    else:
        raise ValueError(f"Unsupported browser: {browser_type}")

    driver.maximize_window()
    driver.delete_all_cookies()

    main_page = pages.main_page.MainPage(driver)
    main_page.open_url_accept_cookie()

    driver.implicitly_wait(5)
    yield driver

    driver.quit()


def pytest_addoption(parser):
    parser.addoption(
        '--headless',
        action='store',
        default='no',
        help='Run browser in headless mode: yes or no'
    )
    parser.addoption(
        '--browser',
        action='store',
        default='chrome',
        help='Choose browser to run tests: chrome or firefox'
    )


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

    if rep.when == "call":
        item.rep_call = rep


def pytest_sessionstart(session):
    logs_dir = "allure_logs"
    if os.path.exists(logs_dir):
        shutil.rmtree(logs_dir)
    os.makedirs(logs_dir, exist_ok=True)

import os
import logging
from logging.handlers import RotatingFileHandler
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import pages
from datetime import datetime

LOG_DIR = 'logger'
LOG_FILE = 'test_results_ui.log'
SCREENSHOTS_DIR = 'screenshots'


def setup_logger():
    global logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('UI_Tests_Logger')
    log_file_path = os.path.join(LOG_DIR, LOG_FILE)
    file_handler = RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=2)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


@pytest.fixture(autouse=True)
def driver(request):
    headless_option = request.config.getoption('--headless')
    browser_option = request.config.getoption('--browser')
    driver = create_driver(browser_option, headless_option)
    driver.delete_all_cookies()
    driver.implicitly_wait(5)
    main_page = pages.MainPage(driver)
    main_page.open_url_accept_cookie()
    yield driver
    driver.quit()


def create_driver(browser, headless):
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        if headless == 'yes':
            options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless == 'yes':
            options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    if 'driver' in item.fixturenames and (report.when == 'call' or report.when == 'setup'):
        driver = item.funcargs['driver']
        if not os.path.exists(SCREENSHOTS_DIR):
            os.makedirs(SCREENSHOTS_DIR)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        screenshot_name = f"{report.nodeid.replace('::', '_').replace('/', '_').replace(' ', '_')}_{timestamp}.png"
        screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
        driver.save_screenshot(screenshot_path)
        logger.info(f"Скриншот сохранен: {screenshot_path}")


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


def pytest_sessionstart(session):
    for directory in [LOG_DIR, SCREENSHOTS_DIR, 'allure_logs']:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)
    setup_logger()


def pytest_addoption(parser):
    parser.addoption('--headless', action='store', default='no', help='Run browser in headless mode: yes or no')
    parser.addoption('--browser', action='store', default='chrome',
                     help='Choose browser to run tests: chrome or firefox')

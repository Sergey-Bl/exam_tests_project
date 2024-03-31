import logging
import os
import shutil
from datetime import datetime
from logging.handlers import RotatingFileHandler

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import pages

LOG_DIR = 'logger'
LOG_FILE = 'test_results_ui.log'
SCREENSHOTS_DIR = 'screenshots'


def setup_logger():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    log_file_path = os.path.join(LOG_DIR, LOG_FILE)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=2)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


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

    if report.when == 'call':
        if report.passed:
            logger.info(f"Тест успешно пройден: {item.nodeid}")
        elif report.failed:
            error_msg = report.longreprtext if report.longreprtext else "Ошибка не определена"
            logger.error(f"Тест провален: {item.nodeid}, Причина: {error_msg}")
        elif report.skipped:
            reason = report.wasxfail if report.wasxfail else "Причина не указана"
            logger.warning(f"Тест пропущен: {item.nodeid}, Причина: {reason}")

    if 'driver' in item.fixturenames and report.when == 'call' and report.failed:
        driver = item.funcargs['driver']
        make_screenshot(driver, item.nodeid)


def make_screenshot(driver, nodeid):
    if not os.path.exists(SCREENSHOTS_DIR):
        os.makedirs(SCREENSHOTS_DIR)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    screenshot_name = f"{nodeid.replace('::', '_').replace('/', '_').replace(' ', '_')}_{timestamp}.png"
    screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
    driver.save_screenshot(screenshot_path)
    logger.info(f"Скриншот сохранен: {screenshot_path}")


def pytest_sessionstart(session):
    directories_to_clear = [LOG_DIR, SCREENSHOTS_DIR, 'allure_logs']
    for directory in directories_to_clear:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)

    global logger
    logger = setup_logger()


def pytest_addoption(parser):
    parser.addoption('--headless', action='store', default='no', help='Run browser in headless mode: yes or no')
    parser.addoption('--browser', action='store', default='chrome',
                     help='Choose browser to run tests: chrome or firefox')

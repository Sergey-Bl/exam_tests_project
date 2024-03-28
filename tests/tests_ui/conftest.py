import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import pages


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


@pytest.fixture(scope='session', autouse=True)
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

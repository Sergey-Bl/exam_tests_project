import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import pages.main_page


# scope='session' пока не работает / нужно решать проблему с вебдрайвервейтом 
# и дублирование данных
@pytest.fixture(autouse=True)
def driver_chrome():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.delete_all_cookies()
    main_page = pages.main_page.MainPage(driver)
    main_page.open_url_accept_cookie()
    yield driver
    driver.close()


@pytest.fixture()
def driver_firefox():
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.maximize_window()
    driver.delete_all_cookies()
    main_page = pages.main_page.MainPage(driver)
    main_page.open_url_accept_cookie()
    yield driver
    driver.close()
    driver.quit()

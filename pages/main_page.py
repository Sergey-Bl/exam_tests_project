from selenium.common import StaleElementReferenceException
import allure
import data
import pages


class MainPageLocators:
    ACCEPT_COOKIE_BUTTON = "//div[contains(@class,'Button-module__buttonText') and contains(text(),'Принять')]"
    SEARCH_FIELD = "//*[@id='catalogSearch']"
    SEARCH_BUTTON = ".Search_searchBtn__Tk7Gw"
    CATALOG_BUTTON = "button.styles_catalogButton__z9L_j"
    CATEGORY_TECHNIQUE_HEADER = ".styles_categoryTitle__q3arD"
    BASKET_COUNTER_ADDED_1_PRODUCT = "//*[@class='headerCartCount' and text()='1']"
    ACCOUNT_BUTTON = '//*[@class="styles_userToolsToggler__c2aHe"]'
    USERNAME_FIELD = '//*[@id="login-email"]'
    PASSWORD_FIELD = '//*[@id="login-password"]'
    LOGIN_BUTTON = '//*[@data-testid="loginButton"]'
    USERNAME_LABEL = '//*[@class="userToolsSubtitle"]'
    LOGIN_TAP = "//*[contains(@class, 'style_baseActionButton__VyAyj')]"
    BASKET_LINK = "//div[contains(@class,'ProfileItem_itemText__h3Pbr') and contains(text(),'Корзина')]"
    EXIT_LINK = '//*[@class="ProfileItem_itemCommon__DJPxF ProfileItem_itemLogout__RFHqc"]'


class MainPage(pages.BasePage):
    def __init__(self, driver):
        super().__init__(driver, data.DOMEN)

    def cookie_accept(self):
        try:
            pages.HelperTests.wait_click_xpath(self.driver,
                                               MainPageLocators.ACCEPT_COOKIE_BUTTON,
                                               5)
        except pages.NoSuchElementException:
            pages.logging.error('no cookie pop-up')
        except pages.TimeoutException:
            pages.logging.error('Timed out waiting for the cookie pop-up')

    def open_url_accept_cookie(self):
        self.open_base_url()
        self.cookie_accept()

    @allure.step("Проверка полной загрузки главной страницы")
    def checker_full_load_page(self):
        try:
            pages.WebDriverWait(self.driver, 10).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
            pages.logging.info("page full load")
        except pages.TimeoutException:
            pages.logging.info("timeout")

    def find_checker_field_result(self):
        search_field = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.SEARCH_FIELD, 5)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.SEARCH_FIELD, 5)
        search_field.send_keys("Adidas")
        pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.SEARCH_FIELD, 5)
        pages.HelperTests.wait_click_css(self.driver, MainPageLocators.SEARCH_BUTTON, 10)

        result_find = pages.HelperTests.get_locator_from_css_wb_wait(self.driver, pages.SearchLocators.SEARCH_RESULT,
                                                                     15)
        search_result_text = result_find.text.strip()

        return search_result_text

    def click_check_catalog_button(self):
        pages.HelperTests.wait_click_css(self.driver, MainPageLocators.CATALOG_BUTTON, 10)
        button_locator = pages.HelperTests.get_locator_from_css_wb_wait(self.driver, MainPageLocators.CATALOG_BUTTON,
                                                                        10)
        text_summary_catalog = pages.HelperTests.get_locator_from_css_wb_wait(self.driver,
                                                                              MainPageLocators.CATEGORY_TECHNIQUE_HEADER,
                                                                              10)
        summary_result = text_summary_catalog.text
        return summary_result, button_locator

    def check_added_product_counter_basket(self):
        counter_check = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                         MainPageLocators.BASKET_COUNTER_ADDED_1_PRODUCT)
        return counter_check

    def clear_search_field(self):

        search_field = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.SEARCH_FIELD, 10)
        search_field.clear()

    def login_test_user(self):
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.LOGIN_BUTTON, 5)
        pages.HelperTests.send_symbols_xpath(self.driver, MainPageLocators.USERNAME_FIELD, 'rubetta5064@awgarstone.com',
                                             5)
        pages.HelperTests.send_symbols_xpath(self.driver, MainPageLocators.PASSWORD_FIELD, 'b3719ec9', 5)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.LOGIN_TAP, 10)

    def tap_check_account_user(self):
        try:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        except StaleElementReferenceException:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                         MainPageLocators.BASKET_LINK, 10
                                                         )
        text_label = pages.HelperTests.get_locator_from_xpath_wb_text_wait(self.driver,
                                                                           MainPageLocators.USERNAME_LABEL,
                                                                           'rubetta5064@awgarstone.com', 10
                                                                           )
        return text_label

    def exit_user(self):
        try:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        except StaleElementReferenceException:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                         MainPageLocators.BASKET_LINK, 10
                                                         )
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.EXIT_LINK, 10)

    def check_login_button(self):
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        login_button = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.LOGIN_BUTTON, 5)
        button_text = login_button.text
        return button_text

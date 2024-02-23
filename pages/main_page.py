import data
import pages.search_page
from pages.__init__ import NoSuchElementException, TimeoutException, WebDriverWait, BasePage, \
    HelperTests, logging


class MainPageLocators:
    ACCEPT_COOKIE_BUTTON = "//div[contains(@class,'Button-module__buttonText') and contains(text(),'Принять')]"
    SEARCH_FIELD = "//*[@id='catalogSearch']"
    SEARCH_BUTTON = ".Search_searchBtn__Tk7Gw"
    CATALOG_BUTTON = "button.styles_catalogButton__z9L_j"
    CATEGORY_TECHNIQUE_HEADER = ".styles_categoryTitle__q3arD"
    BASKET_COUNTER_ADDED_1_PRODUCT = "//*[@class='headerCartCount' and text()='1']"


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, data.DOMEN)

    def cookie_accept(self):
        try:
            HelperTests.wait_click_xpath(self.driver,
                                         MainPageLocators.ACCEPT_COOKIE_BUTTON,
                                         5)
        except NoSuchElementException:
            logging.error('no cookie pop-up')
        except TimeoutException:
            logging.error('Timed out waiting for the cookie pop-up')

    def open_url_accept_cookie(self):
        self.open_base_url()
        self.cookie_accept()

    def checker_full_load_page(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
            logging.info("page full load")
        except TimeoutException:
            logging.info("timeout")

    def find_checker_field_result(self):
        search_field = HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.SEARCH_FIELD, 5)
        search_field.send_keys("Adidas")
        HelperTests.wait_click_css(self.driver, MainPageLocators.SEARCH_BUTTON, 15)
        result_find = HelperTests.get_locator_from_css_wb_wait(self.driver,
                                                               pages.search_page.SearchLocators.SEARCH_RESULT, 15)
        search_result_text = result_find.text.strip()

        return search_result_text

    def click_check_catalog_button(self):
        HelperTests.wait_click_css(self.driver, MainPageLocators.CATALOG_BUTTON, 10)
        button_locator = HelperTests.get_locator_from_css_wb_wait(self.driver, MainPageLocators.CATALOG_BUTTON, 10)
        text_summary_catalog = HelperTests.get_locator_from_css_wb_wait(self.driver,
                                                                        MainPageLocators.CATEGORY_TECHNIQUE_HEADER,
                                                                        10)
        summary_result = text_summary_catalog.text
        return summary_result, button_locator

    def check_added_product_counter_basket(self):
        counter_check = HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                   MainPageLocators.BASKET_COUNTER_ADDED_1_PRODUCT)
        return counter_check

    def clear_search_field(self):

        search_field = HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.SEARCH_FIELD, 10)
        search_field.clear()

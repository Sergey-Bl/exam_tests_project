from selenium.common import TimeoutException

import data
import pages


class SearchLocators:
    SEARCH_RESULT = ".b-content > span"
    PRODUCT_FROM_FIND_RANDOM = ".result__root"
    PRODUCT_FROM_FIND_RANDOM_v2 = ".style_product__xVGB6"
    SEARCH_X_BUTTON = "Search_clearBtn__j9c8N"
    SEARCH_CONTENT_v2 = '//*[@class="l-body"]'
    SEARCH_CONTENT = '//*[@class="l-body  "]'


class SearchPage(pages.BasePage):
    def __init__(self, driver):
        super().__init__(driver, data.DOMEN)

    def click_product_from_find(self):
        try:
            pages.HelperTests.wait_click_css(self.driver, SearchLocators.PRODUCT_FROM_FIND_RANDOM, 10)
        except TimeoutException:
            pages.HelperTests.wait_click_css(self.driver, SearchLocators.PRODUCT_FROM_FIND_RANDOM_v2, 10)

    def cansel_selected_item_search(self):
        pages.HelperTests.wait_click_css(self.driver, SearchLocators.SEARCH_X_BUTTON, 10)

    def find_and_select_product(self):
        pages.main_page.MainPage(self.driver).find_checker_field_result()
        SearchPage(self.driver).click_product_from_find()

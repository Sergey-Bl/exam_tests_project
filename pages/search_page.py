import data
from pages import main_page
from pages.__init__ import BasePage, HelperTests


class SearchLocators:
    SEARCH_RESULT = ".b-content > span"
    PRODUCT_FROM_FIND_RANDOM = ".mindbox-pr-view.result__link"
    SEARCH_X_BUTTON = "Search_clearBtn__j9c8N"


class SearchPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, data.DOMEN)

    def click_product_from_find(self):
        HelperTests.wait_click_css(self.driver, SearchLocators.PRODUCT_FROM_FIND_RANDOM, 10)

    def cansel_selected_item_search(self):
        HelperTests.wait_click_css(self.driver, SearchLocators.SEARCH_X_BUTTON, 10)

    def find_and_select_product(self):
        main_page.MainPage(self.driver).find_checker_field_result()
        SearchPage(self.driver).click_product_from_find()

import data
from pages import BasePage, HelperTests


class BasketPageLocators:
    BASKET_BUTTON = ".headerCartBox"
    EMPTY_BASKET_HEADER = ".EmptyBasket_title__fTZV_"
    V21_LOGO_FROM_BASKET = ".logotypeImg"


class BasketPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, data.DOMEN)

    def click_basket(self):
        HelperTests.wait_click_css(self.driver, BasketPageLocators.BASKET_BUTTON, 5)

    def check_empty_basket_result(self):
        path_text_empty_basket = HelperTests.get_locator_from_css_wb_wait(self.driver,
                                                                          BasketPageLocators.EMPTY_BASKET_HEADER, 5)
        return path_text_empty_basket

    def click_here_link_empty_basket(self):
        HelperTests.wait_click_css(self.driver, BasketPageLocators.V21_LOGO_FROM_BASKET)

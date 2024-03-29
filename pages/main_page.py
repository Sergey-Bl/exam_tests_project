import random
import allure
import data
import pages
from selenium.common import StaleElementReferenceException, TimeoutException


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
    EDIT_AC_BUTTON = "//div[contains(@class,'ProfileItem_itemText__h3Pbr') and contains(text(),'Личные данные')]"
    BONUS_LINK_AC = "//div[contains(@class,'ProfileItem_itemText__h3Pbr') and contains(text(),'Бонусный счет')]"
    BONUS_TITLE = '//*[@class="BonusScreen_title__wEsyO"]'
    BONUS_STATUS = '//*[@class="Status_bonusAmount__bMZMF"]'
    EDIT_DATA_USER = '//*[@data-testid="editData"]'
    EDIT_NAME_USER_FIELD = '//*[@label ="Имя"]'
    SAVE_EDIT_US_VALUE = '//*[@class="Button-module__button Button-module__blue-primary"]'
    CONTENT_EDITED_VALUE = '//*[@class="Snackbar-module__content"]'
    PANEL_WITH_NUMBERS = '//*[@class="Contacts_contactsBlockInner__DnPZl"]'
    CONTACT_LINK = "//*[contains(@class,'styles_sitemapItemLink__C33mK') and contains(text(),'Контакты')]"
    FOOTER_VALUE = '//*[@class="styles_legalInformationBlock__iXOVK"]'
    ERROR_LOGIN_MESSAGE = '//*[@class="ErrorMessage-module__message"]'


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
        search_field = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.SEARCH_FIELD, 10)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.SEARCH_FIELD, 5)
        search_field.send_keys("Adidas")
        pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.SEARCH_FIELD, 10)
        pages.HelperTests.wait_click_css(self.driver, MainPageLocators.SEARCH_BUTTON, 10)

    def receiver_value_search(self):
        try:
            result_find = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                           pages.SearchLocators.SEARCH_CONTENT,
                                                                           5)
        except TimeoutException:
            result_find = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                           pages.SearchLocators.SEARCH_CONTENT_v2,
                                                                           5)
        search_result_text = result_find.text

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

    def login_test_user(self, email, password):
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.LOGIN_BUTTON, 5)
        pages.HelperTests.send_symbols_xpath(self.driver, MainPageLocators.USERNAME_FIELD, email,
                                             5)
        pages.HelperTests.send_symbols_xpath(self.driver, MainPageLocators.PASSWORD_FIELD, password, 5)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.LOGIN_TAP, 10)

    def login_test_incorrect_user(self, email, password):
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.LOGIN_BUTTON, 5)
        pages.HelperTests.send_symbols_xpath(self.driver, MainPageLocators.USERNAME_FIELD, email, 5)
        pages.HelperTests.send_symbols_xpath(self.driver, MainPageLocators.PASSWORD_FIELD, password, 5)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.LOGIN_TAP, 10)

    def receive_info_account_user(self):
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

    @allure.description("Выход юзера через глав меню")
    def exit_user(self):
        try:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        except StaleElementReferenceException:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                         MainPageLocators.BASKET_LINK, 10
                                                         )
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.EXIT_LINK, 10)

    @allure.description("Получение и отдача атрибута текста из локатора")
    def receive_login_text_attr(self):
        try:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        except StaleElementReferenceException:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        login_button = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.LOGIN_BUTTON, 5)
        button_text = login_button.get_attribute("textContent").strip()
        return button_text

    @allure.description("переход в изменения личных данных юзера")
    def move_to_account_edit(self):
        try:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        except StaleElementReferenceException:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 5)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.EDIT_AC_BUTTON, 50)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.EDIT_DATA_USER, 5)

    @allure.description("изменения пользовательских данных аккаунта")
    def change_user_value(self):
        def generate_random_string(word):
            word_list = list(word)
            random.shuffle(word_list)
            return ''.join(word_list)

        unique_text = generate_random_string("test")
        pages.HelperTests.send_symbols_xpath(self.driver, MainPageLocators.EDIT_NAME_USER_FIELD, unique_text)

        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.SAVE_EDIT_US_VALUE, 5)

        text_successful = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                           MainPageLocators.CONTENT_EDITED_VALUE, 2)

        text_receive = text_successful.text
        return text_receive

    @allure.description("переход в юзер бонусы")
    def move_to_account_bonus(self):
        try:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 10)
        except StaleElementReferenceException:
            pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.ACCOUNT_BUTTON, 10)
        pages.HelperTests.wait_click_xpath(self.driver, MainPageLocators.BONUS_LINK_AC, 5)

    @allure.description("Получение информации об нахождении айтемов на бонус странице")
    def receive_values_bonus_page(self):
        test_title_bonus = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.BONUS_TITLE,
                                                                            5)
        test_status_bonus = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver, MainPageLocators.BONUS_STATUS,
                                                                             5)
        text_bonus_receive = test_title_bonus.text
        text_status_bonus = test_status_bonus.text
        return text_bonus_receive, text_status_bonus

    @allure.description("Получение данных с номерами на главном экране и передача")
    def receive_text_numbers(self):
        test_text_numbers = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                             MainPageLocators.PANEL_WITH_NUMBERS,
                                                                             5)
        text_numbers = test_text_numbers.text
        return text_numbers

    @allure.description("Переход на страницу контакты")
    def move_to_contact_page(self):
        pages.HelperTests.wait_click_xpath(self.driver,
                                           MainPageLocators.CONTACT_LINK,
                                           10)

    @allure.description("Получение данные в футере")
    def receive_sent_value_footer(self):
        footer_text = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                       MainPageLocators.FOOTER_VALUE,
                                                                       10)
        text_footer = footer_text.text
        return text_footer

    @allure.description("Получение данных не некоректном входе")
    def receive_error_message(self):
        message_error = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                         MainPageLocators.ERROR_LOGIN_MESSAGE,
                                                                         10)
        error_message = message_error.text
        return error_message

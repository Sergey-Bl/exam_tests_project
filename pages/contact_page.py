import pages
import data


class ContactPageLocators:
    FULL_PAGE_CONTENT = '//*[@class="b-content"]'
    CONTACT_US_BUTTON = '//*[@class="g-btn g-button b-write-us-btn"]'
    CONTACT_US_POP_UP = '//*[@class="styles_form__2wk9O"]'
    CONTACT_SENT_BUTTON = "//div[contains(@class,'Button-module__buttonText') and contains(text(),'Отправить')]"


class ContactPage(pages.BasePage):
    def __init__(self, driver):
        super().__init__(driver, data.DOMEN)

    def receive_full_content_page(self):
        content_contact = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                           ContactPageLocators.FULL_PAGE_CONTENT,
                                                                           5)
        contact_page = content_contact.text
        return contact_page

    def receive_content_aft_tap_contact_us(self):
        pages.HelperTests.wait_click_xpath(self.driver,
                                           ContactPageLocators.CONTACT_US_BUTTON, 5)
        contact_info = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                        ContactPageLocators.CONTACT_US_POP_UP, 5)
        contact_sent_button = pages.HelperTests.get_locator_from_xpath_wb_wait(self.driver,
                                                                               ContactPageLocators.CONTACT_US_POP_UP, 5)
        contact_pop_up_info = contact_info.text
        return contact_pop_up_info, contact_sent_button

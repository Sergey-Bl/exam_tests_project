from helpers.__init__ import By, EC, WebDriverWait, ActionChains, Keys


# ---------------------------------------------------------------
# CSS
class HelperTests:
    def __init__(self, driver):
        self.driver = driver

    def get_from_css(self, selector):
        return f'[class="{selector}"]'

    def get_locator_from_class_css(self, selector):
        selector = self.get_from_css(selector)
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def get_locator_from_css(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def get_locator_from_css_wb_wait(self, selector, timeout=5):
        css = selector
        locator = (By.CSS_SELECTOR, css)

        return WebDriverWait(self, timeout).until(
            EC.presence_of_element_located(locator)
        )

    # ---------------------------------------------------------------
    # XPath

    def get_from_xpath(self, selector):
        return f'//*[contains(@class, "{selector}")]'

    def get_locator_from_class_xpath(self, selector):
        selector = self.get_from_xpath(selector)
        return self.driver.find_element(By.XPATH, selector)

    def get_locator_from_xpath(self, selector):
        return self.driver.find_element(By.XPATH, selector)

    def get_locator_from_xpath_elements(self, selector):
        return self.driver.find_elements(By.XPATH, selector)

    def get_from_data_id_xpath(self, data_id):
        return f'//*[data-id="{data_id}"]'

    def get_locator_from_xpath_wb_wait(self, selector, timeout=5):
        xpath = selector
        locator = (By.XPATH, xpath)

        return WebDriverWait(self, timeout).until(
            EC.presence_of_element_located(locator)
        )

    # -----------
    # CLICKS
    def wait_click_xpath(self, selector, timeout=5):
        xpath = selector
        locator = (By.XPATH, xpath)

        return WebDriverWait(self, timeout).until(
            EC.presence_of_element_located(locator)
        ).click()

    def wait_click_css(self, selector, timeout=5):
        css = selector
        locator = (By.CSS_SELECTOR, css)

        return WebDriverWait(self, timeout).until(
            EC.presence_of_element_located(locator)
        ).click()

    def force_click(self, locator):
        element = self.get_locator_from_xpath(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def click_on(self, locator):
        print(f'click on {locator}')
        element = self.driver.find_element(By.XPATH, locator)
        element.click()

    def click_mouse(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        actions = ActionChains(self.driver)
        actions.click(element).perform()

    def click_with_keyboard(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        element.send_keys(Keys.ENTER)

    # send/clear keys
    def send_symbols(self, locator_x, symbols, timeout=10):
        locator = (By.XPATH, locator_x)

        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)).send_keys(symbols)

    def clear_symbols(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        element.clear()

    def get_value(self, locator):
        element = self.driver.find_element(By.XPATH, locator)

        field_value = element.get_attribute('value')
        print(field_value)
        return field_value

    # asserts helps
    def assert_title(self, expected_title):
        actual_title = self.driver.title
        assert actual_title == expected_title, f"Expected title:{expected_title}, byt got {actual_title}"

    def assert_element_text(self, element, expected_text):
        actual_text = element
        assert expected_text == actual_text, f"Expected text: {expected_text}, but got: {actual_text}"

    def assert_text_in_locator(self, locator, expected_text, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        actual_text = element
        assert actual_text == expected_text, f"Expected text: {expected_text}, but got: {actual_text}"

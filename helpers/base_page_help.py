from helpers.__init__ import By, EC, WebDriverWait, ActionChains, Keys, allure


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

    @allure.step("Получение  и ожидание локатора xpath")
    def get_locator_from_xpath_wb_wait(self, selector, timeout=5):
        xpath = selector
        locator = (By.XPATH, xpath)

        return WebDriverWait(self, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Получение и ожидание текста в локаторе xpath")
    def get_locator_from_xpath_wb_text_wait(self, selector, text, timeout=10):
        xpath = selector
        locator = (By.XPATH, xpath)

        WebDriverWait(self, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
        return WebDriverWait(self, timeout).until(
            EC.presence_of_element_located(locator)
        )

    # -----------
    # CLICKS
    @allure.step("Клик с ожиданием xpath")
    def wait_click_xpath(self, selector, timeout=5):
        xpath = selector
        locator = (By.XPATH, xpath)

        element = WebDriverWait(self, timeout).until(
            EC.element_to_be_clickable(locator)
        )

        element.click()

    @allure.step("Клик с ожиданием xpath и использование visable")
    def wait_click_xpath_visible(self, selector, timeout=5):
        xpath = selector
        locator = (By.XPATH, xpath)

        element = WebDriverWait(self, timeout).until(
            EC.visibility_of_element_located(locator)
        )

        element.click()

    @allure.step("Клик с ожиданием css")
    def wait_click_css(self, selector, timeout=5):
        css = selector
        locator = (By.CSS_SELECTOR, css)

        return WebDriverWait(self, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()

    @allure.step("JS клик xpath")
    def force_click(self, locator):
        element = self.get_locator_from_xpath(locator)
        self.execute_script("arguments[0].click();", element)

    @allure.step("JS клик css")
    def force_click_css(self, locator):
        element = self.get_locator_from_css(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Обычный клик xpath")
    def click_on_xpath(self, locator):
        print(f'click on {locator}')
        element = self.find_element(By.XPATH, locator)
        element.click()

    @allure.step("Обычный клик CSS")
    def click_on_css(self, locator):
        print(f'click on {locator}')
        element = self.find_element(By.CSS_SELECTOR, locator)
        element.click()

    @allure.step("Нажатие мышкой")
    def click_mouse(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        actions = ActionChains(self.driver)
        actions.click(element).perform()

    @allure.step("Нажатие с клавиатуры XPATH")
    def click_with_keyboard_xpath(self, locator):
        element = self.find_element(By.XPATH, locator)
        element.send_keys(Keys.ENTER)

    @allure.step("Нажатие с клавиатуры XPATH")
    def click_with_keyboard_css(self, locator):
        element = self.find_element(By.CSS_SELECTOR, locator)
        element.send_keys(Keys.ENTER)

    # send/clear keys
    @allure.step("Отправка символов в поле xpath")
    def send_symbols_xpath(self, locator_xpath, symbols, timeout=10):
        element = WebDriverWait(self, timeout).until(
            EC.visibility_of_element_located((By.XPATH, locator_xpath))
        )
        element.send_keys(symbols)

    @allure.step("Отправка символов в поле css")
    def send_symbols_css(self, locator_css, symbols, timeout=10):
        element = WebDriverWait(self, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, locator_css))
        )
        element.send_keys(symbols)

    @allure.step("Отчистка поля")
    def clear_symbols(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        element.clear()

    def get_value(self, locator):
        element = self.driver.find_element(By.XPATH, locator)

        field_value = element.get_attribute('value')
        print(field_value)
        return field_value

    # asserts helps
    @allure.step("Проверка заголовка страницы")
    def assert_title(self, expected_title):
        actual_title = self.title
        assert actual_title == expected_title, f"Expected title:{expected_title}, byt got {actual_title}"

    @staticmethod
    @allure.step("Сравнение текста полученного с ассерт заложенным")
    def assert_element_text(actual_text, expected_text):
        assert expected_text == actual_text, f"Expected text: {expected_text}, but got: {actual_text}"

    @staticmethod
    @allure.step("Проверка наличия определенных фрагментов текста")
    def assert_contains_all(text, required_fragments):
        missing_fragments = [fragment for fragment in required_fragments if fragment not in text]
        assert not missing_fragments, f"Текст не содержит следующие фрагменты: {missing_fragments}"

    @staticmethod
    @allure.step("Проверка наличия одного из ожидаемых фрагментов текста")
    def assert_contains_any(text, possible_fragments):
        if not any(fragment in text for fragment in possible_fragments):
            assert False, f"Ни один из ожидаемых фрагментов не найден в тексте: {possible_fragments}"

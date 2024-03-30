import logging
import re

import allure
import pytest

from helpers.base_page_help import HelperTests
import data.value_for_tests
import pages.basket_page
import pages.contact_page
import pages.main_page
import pages.product_page
import pages.search_page


@allure.title("Тест-001: Проверка заголовка главной страницы 21vek.by")
@pytest.mark.smoke()
def test_smoke_open_site_21vek(driver):
    pages.main_page.MainPage(driver).checker_full_load_page()
    HelperTests.assert_title(driver, 'Онлайн-гипермаркет 21vek.by')


@allure.title("Тест-002: Проверка поиска товаров")
@pytest.mark.search()
def test_search_func(driver):
    pages.main_page.MainPage(driver).find_checker_field_result()
    search_result_text = pages.main_page.MainPage(driver).receiver_value_search()

    expected_fragments = [
        'Запрос «adidas». Найдено? \d+ товар(?:ов)?',
        'Результаты поиска'
    ]
    matches_any = any(re.search(pattern, search_result_text, re.IGNORECASE) for pattern in expected_fragments)
    assert matches_any, f"Текст не соответствует ни одному из ожидаемых шаблонов: {expected_fragments}"


@allure.title("Тест-003: Проверка открытия каталогов/состояния кнопки каталога")
@pytest.mark.catalog()
def test_catalog_open(driver):
    button_locator = pages.main_page.MainPage(driver).click_check_catalog_button()

    assert 'styles_pressed__kCcrg' in button_locator.get_attribute('class')


@allure.title("Тест-004: Проверка открытия корзины без наполнения")
@pytest.mark.basket()
def test_open_empty_basket(driver):
    pages.basket_page.BasketPage(driver).click_basket()
    path_text_empty_basket = pages.basket_page.BasketPage(driver).check_empty_basket_result()
    text_empty_basket = path_text_empty_basket.text
    HelperTests.assert_element_text(text_empty_basket, 'Корзина пуста')


@allure.title("Тест-005: Открытие корзины и уход с корзины на глав сцену")
@pytest.mark.basket()
def test_open_link_from_empty_basket(driver):
    pages.basket_page.BasketPage(driver).click_basket()
    pages.basket_page.BasketPage(driver).check_empty_basket_result()
    pages.basket_page.BasketPage(driver).click_here_link_empty_basket()
    pages.main_page.MainPage(driver).checker_full_load_page()
    HelperTests.assert_title(driver, 'Онлайн-гипермаркет 21vek.by')


@allure.title("Тест-006: Добавление продукта в корзину и проверка что продукт в корзине/каунтер +1")
@pytest.mark.basket()
def test_add_product_from_product_page(driver):
    pages.search_page.SearchPage(driver).find_and_select_product()
    pages.product_page.ProductPage(driver).click_add_to_basket()
    counter_check = pages.main_page.MainPage(driver).check_added_product_counter_basket()
    element_product_basket_check = pages.product_page.ProductPage(driver).check_after_added_product()
    HelperTests.assert_element_text(element_product_basket_check.text, 'В корзине')
    assert counter_check is not None and counter_check.text == '1'


@allure.title("Тест-007: Добавление продукта в сравнение")
@pytest.mark.product()
def test_add_to_comparison(driver):
    pages.search_page.SearchPage(driver).find_and_select_product()
    pages.product_page.ProductPage(driver).click_campare_link_add_remove()
    check_available_campare, check_counter_campare = pages.product_page.ProductPage(
        driver).campare_added_products_check()
    if not check_available_campare.is_enabled():
        logging.error("Element is not active after add product")
    assert check_available_campare.is_enabled()
    assert check_counter_campare.is_enabled()


@allure.title("Тест-008: Добавление продукта в избранное")
@pytest.mark.product()
def test_add_in_favorite(driver):
    pages.search_page.SearchPage(driver).find_and_select_product()
    favorite_element = pages.product_page.ProductPage(driver).favorite_link_click()
    HelperTests.assert_element_text(favorite_element.text, 'Удалить из избранного')
    assert 'putaside__link j-putaside j-putaside__in' in favorite_element.get_attribute('class')


@allure.title("Тест-009: Проверка открытия и доступность поп апа/полей при добавлении мнения")
@pytest.mark.product()
def test_open_opinion_module(driver):
    pages.search_page.SearchPage(driver).find_and_select_product()
    pages.product_page.ProductPage(driver).opinion_link_click()
    pages.product_page.ProductPage(driver).add_opinion_click()
    name_opinion, description_opinion, phone_opinion, sent_button_opinion = pages.product_page.ProductPage(
        driver).check_fields_opinion()
    assert name_opinion is not None
    assert description_opinion is not None
    assert phone_opinion is not None
    assert sent_button_opinion is not None


@allure.title("Тест-010: Проверка загрузки картинки продукта")
@pytest.mark.product()
def test_open_image_product(driver):
    pages.search_page.SearchPage(driver).find_and_select_product()
    pages.product_page.ProductPage(driver).click_image_product()
    x_image_button, image_panel = pages.product_page.ProductPage(driver).check_image_panel()
    assert x_image_button is not None
    assert image_panel is not None


@pytest.mark.parametrize("email,password", [
    ('rubetta5064@awgarstone.com', 'b3719ec9')
])
@allure.title("Тест-011: Логирование тестовым юзером")
@pytest.mark.user()
def test_login_test_user(driver, email, password):
    pages.main_page.MainPage(driver).login_test_user(email, password)
    text_label = pages.main_page.MainPage(driver).receive_info_account_user()
    text_expected = text_label.text
    HelperTests.assert_element_text(text_expected, 'rubetta5064@awgarstone.com')


@pytest.mark.parametrize("email,password", [
    ('rubetta5064@awgarstone.com', 'b3719ec9')
])
@allure.title("Тест-012: Добавление продукта авторизированным юзером")
@pytest.mark.user()
def test_login_and_add_product(driver, email, password):
    pages.main_page.MainPage(driver).login_test_user(email, password)
    pages.main_page.MainPage(driver).receive_info_account_user()
    pages.search_page.SearchPage(driver).find_and_select_product()
    pages.product_page.ProductPage(driver).click_add_to_basket()
    counter_check = pages.main_page.MainPage(driver).check_added_product_counter_basket()
    element_product_basket_check = pages.product_page.ProductPage(driver).check_after_added_product()
    HelperTests.assert_element_text(element_product_basket_check.text, 'В корзине')
    assert counter_check is not None and counter_check.text == '1'

    pages.basket_page.BasketPage(driver).click_basket()
    pages.basket_page.BasketPage(driver).remove_from_basket_product()
    path_text_empty_basket = pages.basket_page.BasketPage(driver).check_empty_basket_result()
    text_empty_basket = path_text_empty_basket.text
    HelperTests.assert_element_text(text_empty_basket, 'Корзина пуста')


@pytest.mark.parametrize("email,password", [
    ('rubetta5064@awgarstone.com', 'b3719ec9')
])
@allure.title("Тест-013: Вылогирование юзера")
@pytest.mark.user()
def test_exit_user(driver, email, password):
    pages.main_page.MainPage(driver).login_test_user(email, password)
    pages.main_page.MainPage(driver).exit_user()
    button_text = pages.main_page.MainPage(driver).receive_login_text_attr()
    HelperTests.assert_element_text(button_text, 'Войти')


@pytest.mark.parametrize("email,password", [
    ('rubetta5064@awgarstone.com', 'b3719ec9')
])
@allure.title("Тест-014: Смена личных данных юзера")
@allure.description("В headless моде ошибка / появляется чекбокс к поп апе который невозможно отловить вне хедлес мода,"
                    "защита какая-то или баг, обойти пока не вышло")
@pytest.mark.user()
def test_edit_user_value(driver, email, password):
    pages.main_page.MainPage(driver).login_test_user(email, password)
    pages.main_page.MainPage(driver).move_to_account_edit()
    text_receive = pages.main_page.MainPage(driver).change_user_value()
    HelperTests.assert_element_text(text_receive, 'Личные данные изменены')


@pytest.mark.parametrize("email,password", [
    ('rubetta5064@awgarstone.com', 'b3719ec9')
])
@allure.title("Тест-015: Доступности бонус счета")
@pytest.mark.user()
def test_bonus_availability(driver, email, password):
    pages.main_page.MainPage(driver).login_test_user(email, password)
    pages.main_page.MainPage(driver).move_to_account_bonus()
    text_bonus_receive, text_status_bonus = pages.main_page.MainPage(driver).receive_values_bonus_page()
    HelperTests.assert_element_text(text_bonus_receive, 'Бонусный счёт')
    HelperTests.assert_element_text(text_status_bonus, '0 бонусов')


@allure.title("Тест-016: Доступности номеров компании")
@pytest.mark.user()
def test_number_company_availability(driver):
    text_numbers = pages.main_page.MainPage(driver).receive_text_numbers()
    required_numbers = data.value_for_tests.value_for_test_16
    HelperTests.assert_contains_all(text_numbers, required_numbers)


@allure.title("Тест-017 Доступности элементов на странице контактов")
@pytest.mark.contact_us()
def test_content_contact_page(driver):
    pages.main_page.MainPage(driver).move_to_contact_page()
    contact_page = pages.contact_page.ContactPage(driver).receive_full_content_page()
    required_value = data.value_for_tests.value_for_test_17
    HelperTests.assert_contains_all(contact_page, required_value)


@allure.title("Тест-018 Доступность элементов/текста поп апа 'Написать нам'")
@pytest.mark.contact_us()
def test_content_contact_pop_up(driver):
    pages.main_page.MainPage(driver).move_to_contact_page()
    content_pop_up, contact_sent_button = pages.contact_page.ContactPage(driver).receive_content_aft_tap_contact_us()
    required_value = data.value_for_tests.value_for_test_18
    HelperTests.assert_contains_all(content_pop_up, required_value)
    assert contact_sent_button.is_displayed()


@allure.title("Тест-019 Футтер текст")
@pytest.mark.footer()
def test_footer(driver):
    text_footer = pages.main_page.MainPage(driver).receive_sent_value_footer()
    required_value = data.value_for_tests.value_for_test_19
    HelperTests.assert_contains_all(text_footer, required_value)


@pytest.mark.parametrize("email,password,expected_error", [
    ('123456', 'password', 'Неправильный формат электронной почты'),
    ('test@example.com', 'wrongpassword', 'Нет такого аккаунта. \nЗарегистрироваться?')
])
@allure.title("Тест-020: Вход с невалидными данными")
@pytest.mark.user()
def test_enter_incorrect_value(driver, email, password, expected_error):
    pages.main_page.MainPage(driver).login_test_incorrect_user(email, password)
    error_message = pages.main_page.MainPage(driver).receive_error_message()
    HelperTests.assert_element_text(error_message, expected_error)

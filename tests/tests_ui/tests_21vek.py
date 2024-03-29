import re
import allure
import pytest
import pages.basket_page
import pages.main_page
import pages.product_page
import pages.search_page
import logging

from helpers.base_page_help import HelperTests


@allure.title("Тест-001: Проверка заголовка главной страницы 21vek.by")
@pytest.mark.smoke()
def test_smoke_open_site_21vek(driver):
    pages.main_page.MainPage(driver).checker_full_load_page()
    HelperTests.assert_title(driver, 'Онлайн-гипермаркет 21vek.by')


@allure.title("Тест-002: Проверка поиска товаров")
@pytest.mark.search()
def test_search_func(driver):
    search_result_text = pages.main_page.MainPage(driver).find_checker_field_result()
    pattern = re.compile(r'Запрос «adidas». Найдено? \d+ товар(?:ов)?', re.IGNORECASE)
    assert pattern.match(search_result_text) is not None


@allure.title("Тест-003: Проверка открытия каталогов/состояния кнопки каталога")
@pytest.mark.basket()
def test_catalog_open(driver):
    summary_result, button_locator = pages.main_page.MainPage(driver).click_check_catalog_button()

    assert 'styles_pressed__kCcrg' in button_locator.get_attribute('class')
    HelperTests.assert_element_text(driver, summary_result, 'Бытовая техника')


@allure.title("Тест-004: Проверка открытия корзины без наполнения")
@pytest.mark.basket()
def test_open_empty_basket(driver):
    pages.basket_page.BasketPage(driver).click_basket()
    path_text_empty_basket = pages.basket_page.BasketPage(driver).check_empty_basket_result()
    text_empty_basket = path_text_empty_basket.text
    HelperTests.assert_element_text(driver, text_empty_basket, 'Корзина пуста')


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
    HelperTests.assert_element_text(driver, element_product_basket_check.text, 'В корзине')
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
    assert 'putaside__link j-putaside j-putaside__in' in favorite_element.get_attribute('class')
    assert favorite_element.text == "Удалить из избранного"


@allure.title("Тест-009: Проверка открытия и доступность поп апа/полей при добавлении мнения")
@pytest.mark.product("test-009")
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


@allure.title("Тест-011: Логирование тестовым юзером")
@pytest.mark.user()
def test_login_test_user(driver):
    pages.main_page.MainPage(driver).login_test_user()
    text_label = pages.main_page.MainPage(driver).tap_check_account_user()
    text_expected = text_label.text
    HelperTests.assert_element_text(driver, text_expected, 'rubetta5064@awgarstone.com')


@allure.title("Тест-012: Добавление продукта авторизированным юзером")
@pytest.mark.user()
def test_login_and_add_product(driver):
    pages.main_page.MainPage(driver).login_test_user()
    pages.main_page.MainPage(driver).tap_check_account_user()
    pages.search_page.SearchPage(driver).find_and_select_product()
    pages.product_page.ProductPage(driver).click_add_to_basket()
    counter_check = pages.main_page.MainPage(driver).check_added_product_counter_basket()
    element_product_basket_check = pages.product_page.ProductPage(driver).check_after_added_product()
    HelperTests.assert_element_text(driver, element_product_basket_check.text, 'В корзине')
    assert counter_check is not None and counter_check.text == '1'

    pages.basket_page.BasketPage(driver).click_basket()
    pages.basket_page.BasketPage(driver).remove_from_basket_product()
    path_text_empty_basket = pages.basket_page.BasketPage(driver).check_empty_basket_result()
    text_empty_basket = path_text_empty_basket.text
    HelperTests.assert_element_text(driver, text_empty_basket, 'Корзина пуста')


@allure.title("Тест-013: Вылогирование юзера")
@pytest.mark.user()
def test_exit_user(driver):
    pages.main_page.MainPage(driver).login_test_user()
    pages.main_page.MainPage(driver).exit_user()
    button_text = pages.main_page.MainPage(driver).check_login_button()
    assert button_text == "Аккаунт", f"Текст кнопки не соответствует ожидаемому. Актуальный текст: '{button_text}'"

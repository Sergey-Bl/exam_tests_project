import re

import pytest
import pages.basket_page
import pages.main_page
import pages.product_page
import pages.search_page
import logging


@pytest.mark.smoke("test-001")
def test_smoke_open_site_21vek(driver_chrome):
    pages.main_page.MainPage(driver_chrome).checker_full_load_page()
    assert driver_chrome.title == 'Онлайн-гипермаркет 21vek.by'


@pytest.mark.search("test-002")
def test_search_func(driver_chrome):
    search_result_text = pages.main_page.MainPage(driver_chrome).find_checker_field_result()
    pattern = re.compile(r'Запрос «adidas». Найдено? \d+ товар(?:ов)?', re.IGNORECASE)
    assert pattern.match(search_result_text) is not None


@pytest.mark.basket("test-003")
def test_catalog_open(driver_chrome):
    summary_result, button_locator = pages.main_page.MainPage(driver_chrome).click_check_catalog_button()

    assert 'styles_pressed__kCcrg' in button_locator.get_attribute('class')
    assert summary_result == 'Бытовая техника'


@pytest.mark.basket("test-004")
def test_open_empty_basket(driver_chrome):
    pages.basket_page.BasketPage(driver_chrome).click_basket()
    path_text_empty_basket = pages.basket_page.BasketPage(driver_chrome).check_empty_basket_result()
    text_empty_basket = path_text_empty_basket.text
    assert text_empty_basket == 'У вас пока нет ни одного товара в корзине,\nвы можете выбрать их здесь'


@pytest.mark.basket("test-005")
def test_open_link_from_empty_basket(driver_chrome):
    test_open_empty_basket(driver_chrome)
    pages.basket_page.BasketPage(driver_chrome).click_here_link_empty_basket()
    pages.main_page.MainPage(driver_chrome).checker_full_load_page()
    assert driver_chrome.title == 'Онлайн-гипермаркет 21vek.by'


@pytest.mark.basket("test-006")
def test_add_product_from_product_page(driver_chrome):
    pages.search_page.SearchPage(driver_chrome).find_and_select_product()
    pages.product_page.ProductPage(driver_chrome).click_add_to_basket()
    counter_check = pages.main_page.MainPage(driver_chrome).check_added_product_counter_basket()
    element_product_basket_check = pages.product_page.ProductPage(driver_chrome).check_after_added_product()
    assert element_product_basket_check.text == 'В корзине'
    assert counter_check is not None and counter_check.text == '1'


@pytest.mark.product("test-007")
def test_add_to_comparison(driver_chrome):
    pages.search_page.SearchPage(driver_chrome).find_and_select_product()
    pages.product_page.ProductPage(driver_chrome).click_campare_link_add_remove()
    check_available_campare, check_counter_campare = pages.product_page.ProductPage(
        driver_chrome).campare_added_products_check()
    if not check_available_campare.is_enabled():
        logging.error("Element is not active after add product")
    assert check_available_campare.is_enabled()
    assert check_counter_campare.is_enabled()


@pytest.mark.product("test-008")
def test_add_in_favorite(driver_chrome):
    pages.search_page.SearchPage(driver_chrome).find_and_select_product()
    favorite_element = pages.product_page.ProductPage(driver_chrome).favorite_link_click()
    assert 'putaside__link j-putaside j-putaside__in' in favorite_element.get_attribute('class')
    assert favorite_element.text == "Удалить из избранного"


@pytest.mark.product("test-009")
def test_open_opinion_module(driver_chrome):
    pages.search_page.SearchPage(driver_chrome).find_and_select_product()
    pages.product_page.ProductPage(driver_chrome).opinion_link_click()
    pages.product_page.ProductPage(driver_chrome).add_opinion_click()
    name_opinion, description_opinion, phone_opinion, sent_button_opinion = pages.product_page.ProductPage(
        driver_chrome).check_fields_opinion()
    assert name_opinion is not None
    assert description_opinion is not None
    assert phone_opinion is not None
    assert sent_button_opinion is not None


@pytest.mark.product("test-010")
def test_open_image_product(driver_chrome):
    pages.search_page.SearchPage(driver_chrome).find_and_select_product()
    pages.product_page.ProductPage(driver_chrome).click_image_product()
    x_image_button, image_panel = pages.product_page.ProductPage(driver_chrome).check_image_panel()
    assert x_image_button is not None
    assert image_panel is not None

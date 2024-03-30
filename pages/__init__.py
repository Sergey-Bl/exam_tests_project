import logging

import allure
import random
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import data
from .base_page import BasePage
from .main_page import MainPage
from .search_page import SearchPage, SearchLocators
from helpers.base_page_help import HelperTests

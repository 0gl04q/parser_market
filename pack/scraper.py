import uuid

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import time
import os

from pack.parser import Parser
from pack.shops import InternetShops

PROFILE_PATH = os.environ['PROFILE_PATH']


class Scraper:
    """ Класс для сбора информации из браузера.

    Этот класс предназначен для сбора данных с веб-страниц с использованием браузера.

    :param query: Поисковой запрос продукта
    :param order: Параметр сортировки
    """

    def __init__(self, query: str, order: uuid.UUID, shop=None):

        if shop is None:
            self.shop = InternetShops.megamarket

        service = Service(executable_path='geckodriver')

        firefox_profile = FirefoxProfile(PROFILE_PATH)

        options = Options()
        options.profile = firefox_profile
        options.add_argument('--headless')

        self.driver = webdriver.Firefox(service=service, options=options)
        self.query = query
        self.order = order
        self.url = self.__get_url()
        self.__search_product()

    def __get_url(self):
        self.driver.get(self.shop.link)

        time.sleep(5)

        search_box = self.driver.find_element(By.XPATH, '//input[@class="search-field-input"]')
        search_box.send_keys(self.query)
        search_box.send_keys(Keys.ENTER)

        time.sleep(5)

        return self.driver.current_url

    def __get_current_page_url(self, num_page):
        if '?q=' in self.url:
            return f'page-{num_page}/?q='.join(self.url.split('?q=')) + '&sort=1'
        elif '#?related_search=' in self.url:
            return f'page-{num_page}/#?related_search='.join(self.url.split('#?related_search=')) + '&sort=1'

    def __search_product(self):

        source = Parser(self.order, self.shop)

        for num in range(1, 5):
            current_page_url = self.__get_current_page_url(num)

            self.driver.get(current_page_url)

            time.sleep(5)

            source.page_source = self.driver.page_source

            source.update_lists()

        source.create_df()
        source.sort_df('Разница')
        source.send_in_db()

        self.driver.close()

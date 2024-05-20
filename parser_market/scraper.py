import logging
import uuid

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import time
import os

from parser_market.parser import Parser
from parser_market.shops import InternetShops
from parser_market.mailer import one_send_mail
from parser_market.logger import setup_logger

logger = setup_logger(__name__)

PROFILE_PATH = os.environ['PROFILE_PATH']


class Scraper:
    """ Класс для сбора информации из браузера.

    Этот класс предназначен для сбора данных с веб-страниц с использованием браузера.

    :param query: Поисковой запрос продукта
    :param order: Параметр сортировки
    """

    def __init__(self, query: str, order: uuid.UUID, shop=None):

        logger.info(f'run scraper, order: {order}')

        if shop is None:
            self.shop = InternetShops.megamarket

        self.query = query
        self.order = order

        service = Service(executable_path='geckodriver')

        firefox_profile = FirefoxProfile(PROFILE_PATH)

        options = Options()
        options.profile = firefox_profile
        options.add_argument('--headless')

        self.driver = webdriver.Firefox(service=service, options=options)

        logger.info(f'run driver, order: {self.order}')

        try:
            self.url = self.__get_url()
            self.__search_product()

            logger.info(f'success run, order: {self.order}')

        except Exception as e:

            logger.error(f'EXCEPTION - DRIVER FALL, ORDER {self.order}, e = {e}')

            one_send_mail('Падение драйвера', f'Traceback: <p>{e}</p>')

            raise e

        finally:
            self.driver.quit()

    def __get_url(self):

        logger.info(f'get link, order: {self.order}')

        self.driver.get(self.shop.link + self.query)

        time.sleep(5)

        logger.info(f'return main url, order: {self.order}')

        return self.driver.current_url

    def __get_current_page_url(self, num_page):
        if '?q=' in self.url:
            return f'page-{num_page}/?q='.join(self.url.split('?q=')) + '&sort=1'
        elif '#?related_search=' in self.url:
            return f'page-{num_page}/#?related_search='.join(self.url.split('#?related_search=')) + '&sort=1'

    def __search_product(self):

        source = Parser(self.order, self.shop)

        logger.info(f'start parsing url, order: {self.order}')

        for num in range(1, 5):
            current_page_url = self.__get_current_page_url(num)
            self.driver.get(current_page_url)

            logger.info(f'get card on page, order: {self.order}')

            time.sleep(5)

            source.page_source = self.driver.page_source

            logger.info(f'start updating list, order: {self.order}')

            source.update_lists()

        source.create_df()
        logger.info(f'create df, order: {self.order}')

        source.sort_df('Разница')
        logger.info(f'sorted by ..., order: {self.order}')

        source.send_in_db()
        logger.info(f'send in db card, order, {self.order}')

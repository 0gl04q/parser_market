from bs4 import BeautifulSoup
import pandas as pd
import requests

from parser_market.mailer import one_send_mail
from parser_market.logger import setup_logger

logger = setup_logger(__name__)


class Parser:
    """ Класс парсинга и создания xlsx, с возможностью взаимодействовать с элементами в дальнейшем

    :param page_source: Содержание страницы
    :param order: ID заявки
    :shop: Магазин поиска
    """

    def __init__(self, order, shop, page_source=None):

        logger.info(f'init parsing, order: {order}')

        self.order = order
        self.page_source = page_source
        self.shop = shop

        self.names = []
        self.photos = []
        self.price = []
        self.links = []
        self.bonus = []

        self.df = None

        # Получаем значения
        if page_source:
            self.update_lists()

    @staticmethod
    def money_to_int(item):
        return int(''.join(item.split(' ')))

    def update_lists(self):
        """ Функция сбора информации имен, цен, бонусов"""

        logger.info(f'start updated lists, order: {self.order}')

        # Собираем суп
        soup = BeautifulSoup(self.page_source, features="html.parser")

        # Находим каталог товаров
        catalog = soup.find(name=self.shop.parameters.catalog.tag,
                            attrs=self.shop.parameters.catalog.attrs)

        # Выбираем список всех товаров на странице
        items_list = catalog.find_all(name=self.shop.parameters.catalog.tag,
                                      attrs=self.shop.parameters.items.attrs)

        for item in items_list:
            name = item.find(name=self.shop.parameters.name.tag,
                             attrs=self.shop.parameters.name.attrs).text

            photo = item.find(name=self.shop.parameters.photo.tag,
                              attrs=self.shop.parameters.photo.attrs).attrs['src']

            link = item.find(name=self.shop.parameters.link.tag,
                             attrs=self.shop.parameters.link.attrs).attrs['href']

            price = item.find(name=self.shop.parameters.price.tag,
                              attrs=self.shop.parameters.price.attrs).text.rstrip(' ₽')

            price = self.money_to_int(price)

            bonus = item.find(name=self.shop.parameters.bonus.tag,
                              attrs=self.shop.parameters.bonus.attrs)

            bonus = self.money_to_int(bonus.text) if bonus else 0

            self.names.append(name)
            self.photos.append(photo)
            self.links.append(self.shop.main + link)
            self.price.append(price)
            self.bonus.append(bonus)

        self.page_source = None

        logger.info(f'end updated lists, order: {self.order}')

    def count_pages(self, page_source):
        logger.info(f'count pages, order: {self.order}')

        soup = BeautifulSoup(page_source, features='html.parser')

        pager = soup.find(name=self.shop.parameters.pager.tag,
                          attrs=self.shop.parameters.pager.attrs)

        pages_el = pager.find_all(name=self.shop.parameters.page_el.tag)

        count_pages = len(pages_el)

        if count_pages > 5:
            return 5
        return count_pages

    def create_df(self):
        self.df = pd.DataFrame({'Имя': self.names,
                                'Фото': self.photos,
                                'Ссылки': self.links,
                                'Цена': self.price,
                                'Бонусы': self.bonus})

        self.df['Разница'] = self.df['Цена'] - self.df['Бонусы']

    def create_excel(self, name_file: str):
        self.df.to_excel(excel_writer=f'./products/{name_file}.xlsx', index=False)

    def sort_df(self, by: str | list):
        self.df = self.df.sort_values(by=by)

    def clean_in_db(self) -> bool:
        logger.info(f'clean old info, order: {self.order}')

        response = requests.request('delete', f'http://127.0.0.1:8000/api/cards/{self.order}/')

        if response.status_code != 204:
            logger.error(f'ERROR DELETE REQUEST FALL. CHECK EMAIL. ORDER: {self.order}')

            one_send_mail(subject='Ошибка удаления записей',
                          text=f'<p>Произошла ошибка при удалении старых карточек: {response.status_code},</p>'
                               f'<p> Данные по заявке {self.order}</p><br>')
            return False
        return True

    def send_in_db(self):
        if not self.clean_in_db():
            return

        logger.info(f'start send card in db, order: {self.order}')

        data = []

        for index, item in self.df.iterrows():
            if len(data) == 12:
                break

            name, photo, link, price, bonus, real_price = item

            data.append({
                'order': str(self.order),
                'name': name,
                'price': price,
                'bonus': bonus,
                'promo': 0,
                'photo': photo,
                'link': link,
                'real_price': real_price,
            })

        response = requests.request('post', f'http://127.0.0.1:8000/api/cards/{self.order}/', json=data)

        if response.status_code != 201:
            logger.error(f'ERROR SEND REQUEST ON SERVER. CHECK EMAIL. ORDER: {self.order}')

            one_send_mail(
                subject=f'Ошибка {response.status_code}',
                text=f'<p> Произошла ошибка при передаче карточки: {response.status_code}, </p><br>'
                     f'<p> Данные по заявке {self.order}</p><br>'
            )

        logger.info(f'end send cards in db, order: {self.order}')

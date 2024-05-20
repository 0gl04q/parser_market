from bs4 import BeautifulSoup
from mailer import Mail

import pickle
import pandas as pd
import requests


class Parser:
    """ Класс парсинга и создания xlsx, с возможностью взаимодействовать с элементами в дальнейшем

    :param page_source: Содержание страницы
    """

    def __init__(self, order, shop, page_source=None):
        self.order = order
        self.page_source = page_source
        self.shop = shop

        self.names = []
        self.price = []
        self.links = []
        self.bonus = []

        self.df = None
        self.send_counter = None

        # Получаем значения
        if page_source:
            self.update_lists()

    @staticmethod
    def money_to_int(item):
        return int(''.join(item.split(' ')))

    def update_lists(self):
        """ Функция сбора информации имен, цен, бонусов"""

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

            link = item.find(name=self.shop.parameters.link.tag,
                             attrs=self.shop.parameters.link.attrs).attrs['href']

            price = item.find(name=self.shop.parameters.price.tag,
                              attrs=self.shop.parameters.price.attrs).text.rstrip(' ₽')

            price = self.money_to_int(price)

            bonus = item.find(name=self.shop.parameters.bonus.tag,
                              attrs=self.shop.parameters.bonus.attrs)

            bonus = self.money_to_int(bonus.text) if bonus else 0

            self.names.append(name)
            self.links.append(self.shop.link + link)
            self.price.append(price)
            self.bonus.append(bonus)

        self.page_source = None

    def create_df(self):
        self.df = pd.DataFrame({'Имя': self.names,
                                'Ссылки': self.links,
                                'Цена': self.price,
                                'Бонусы': self.bonus})

        self.df['Разница'] = self.df['Цена'] - self.df['Бонусы']

    def create_excel(self, name_file: str):
        self.df.to_excel(excel_writer=f'./products/{name_file}.xlsx', index=False)

    def sort_df(self, by: str | list):
        self.df = self.df.sort_values(by=by)

    def send_in_db(self):
        mail = Mail()

        self.send_counter = 0

        for index, item in self.df.iterrows():
            name, link, price, bonus, real_price = item
            response = requests.request('post', f'http://127.0.0.1:8000/api/cards/{self.order}/', data={
                'order': self.order,
                'name': name,
                'price': price,
                'bonus': bonus,
                'promo': 0,
                'link': link,
                'real_price': real_price,
            })

            if response.status_code != 201:
                mail.send_message(
                    subject=f'Ошибка {response.status_code}',
                    text=f'<p> Произошла ошибка при передаче карточки: {response.status_code}, </p><br>'
                         f'<p> Данные по заявке {self.order}: {item}</p><br>'
                )
            else:
                self.send_counter += 1

        mail.quit_server()

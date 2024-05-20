from dataclasses import dataclass


@dataclass
class Parameter:
    tag: str
    attrs: dict


@dataclass
class ShopParameters:
    catalog: Parameter
    items: Parameter
    name: Parameter
    link: Parameter
    price: Parameter
    bonus: Parameter


@dataclass
class Shop:
    link: str
    parameters: ShopParameters


class InternetShops:
    megamarket = Shop(
        link='https://www.megamarket.ru',
        parameters=ShopParameters(
            catalog=Parameter(
                tag='div',
                attrs={'class': 'catalog-items-list'}
            ),
            items=Parameter(
                tag='div',
                attrs={'class': 'catalog-item-regular-desktop ddl_product catalog-item-desktop'}
            ),
            name=Parameter(
                tag='a',
                attrs={'class': 'catalog-item-regular-desktop__title-link ddl_product_link'}
            ),
            link=Parameter(
                tag='a',
                attrs={'class': 'catalog-item-regular-desktop__title-link ddl_product_link'}
            ),
            price=Parameter(
                tag='div',
                attrs={'class': 'catalog-item-regular-desktop__price'}
            ),
            bonus=Parameter(
                tag='span',
                attrs={'class': 'bonus-amount'}
            )
        )
    )

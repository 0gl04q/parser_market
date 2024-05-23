from dataclasses import dataclass


@dataclass
class Parameter:
    tag: str
    attrs: dict


@dataclass
class ShopParameters:
    catalog: Parameter
    photo: Parameter
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
        link='https://megamarket.ru/catalog/?q=',
        parameters=ShopParameters(
            catalog=Parameter(
                tag='div',
                attrs={'class': 'catalog-items-list'}
            ),
            photo=Parameter(
                tag='img',
                attrs={'data-test': 'product-image'}
            ),
            items=Parameter(
                tag='div',
                attrs={'data-list-id': 'main'}
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

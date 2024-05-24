from dataclasses import dataclass


@dataclass
class Parameter:
    tag: str
    attrs: dict = None


@dataclass
class ShopParameters:
    catalog: Parameter
    items: Parameter

    name: Parameter
    photo: Parameter
    link: Parameter
    price: Parameter
    bonus: Parameter

    pager: Parameter
    page_el: Parameter


@dataclass
class Shop:
    main: str
    link: str
    parameters: ShopParameters


class InternetShops:
    megamarket = Shop(
        main='https://megamarket.ru',
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
            ),
            pager=Parameter(
                tag='ul',
                attrs={'class': 'full'}
            ),
            page_el=Parameter(
                tag='li'
            )
        )
    )

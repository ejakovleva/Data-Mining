import re
from urllib.parse import urljoin

from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def clear_price(price):
    try:
        # result = float(price.replace("\u2009", ""))
        result = float(price)
    except ValueError:
        result = None
    return result


def get_characteristic(item: str) -> dict:
    selector = Selector(text=item)
    data = {
        "name": selector.xpath(
            '//div[contains(@class, "AdvertSpecs_label")]/text()'
        ).extract_first(),
        "value": selector.xpath(
            '//div[contains(@class, "AdvertSpecs_data")]//text()'
        ).extract_first(),
    }
    return data


def get_parameters(item: str) -> dict:
    selector = Selector(text=item)
    data = {
        "name": selector.xpath(
            "//span[contains(@class, 'item-params-label')]/text()"
        ).extract_first(),
        "value": [i for i in selector.xpath("//li[contains(@class, 'item-params-list')]/text()").getall()
                  if i != ' ' and i != '\n  '][0],
    }
    return data


def get_author_id(text):
    re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
    result = re.findall(re_pattern, text)
    try:
        user_link = f"https://youla.ru/user/{result[0]}"
    except IndexError:
        user_link = None
        pass
    return user_link


class AutoyoulaLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    description_out = TakeFirst()
    price_in = MapCompose(clear_price)
    price_out = TakeFirst()
    author_in = MapCompose(get_author_id)
    author_out = TakeFirst()
    # characteristics_in = MapCompose(get_characteristic)


class AvitoLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_in = MapCompose(clear_price)
    price_out = TakeFirst()
    address_out = TakeFirst()
    parameters_in = MapCompose(get_parameters)
    author_out = TakeFirst()



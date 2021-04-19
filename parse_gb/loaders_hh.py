import re
from urllib.parse import urljoin

from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def get_author(author):
    url = 'https://hh.ru/'
    user_link = urljoin(url, author)
    return user_link


def flat_text(items):
    return "".join(items)


def text_with_del(items):
    new_text = "\n".join(items)
    new_text.replace('\n', '', 3)
    return new_text


def make_a_list(item):
    return item[0].split(", ")


class HHLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    description_in = text_with_del
    description_out = text_with_del
    salary_in = flat_text
    salary_out = flat_text
    author_in = MapCompose(get_author)
    author_out = TakeFirst()


class AuthorLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    activity_in = make_a_list
    description_out = TakeFirst()


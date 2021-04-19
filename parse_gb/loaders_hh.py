import re
from urllib.parse import urljoin

from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


class HHLoader(ItemLoader):
    default_item_class = dict
    # url_out = TakeFirst()
    # title_out = TakeFirst()
    # description_out = TakeFirst()
    # price_in = MapCompose(clear_price)
    # price_out = TakeFirst()
    # author_in = MapCompose(get_author_id)
    # author_out = TakeFirst()
    # characteristics_in = MapCompose(get_characteristic)
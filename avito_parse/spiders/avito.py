import re

import scrapy

from avito_parse.loaders import AvitoLoader
from urllib.parse import urljoin

class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ru"]
    start_urls = ["https://www.avito.ru/krasnodar/kvartiry/prodam"]

    _xpath_selectors = {
        "pagination": '//div[contains(@data-marker, "pagination-button")]//span/text()',
        "apartment": "//div[@class='iva-item-titleStep-2bjuh']//a/@href",
    }
    _xpath_data_query = {
        "title": "//span[@class='title-info-title-text']/text()",
        "price": "//span[@class='js-item-price']/text()",
        "address": "//span[@class='item-address__string']/text()",
        "parameters": "//ul[@class='item-params-list//li']",
        "author": "//div[@class='seller-info-name js-seller-info-name']//a/@href",
    }


    def _get_follow_xpath(self, response, selector, callback, **kwargs):
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    # def parse(self, response, *args, **kwargs):
    #     yield from self._get_follow_xpath(
    #         response, self._xpath_selectors["brands"], self.brand_parse
    #     )

    def parse(self, response, **kwargs):
        yield from self._get_follow_xpath(
            response, f'?p={self._xpath_selectors["pagination"]}', self.parse
        )
        yield from self._get_follow_xpath(
            response, self._xpath_selectors["apartment"], self.apartment_parse,
        )

    def apartment_parse(self, response):
        loader = AvitoLoader(response=response)
        loader.add_value("url", response.url)
        for key, selector in self._xpath_data_query.items():
            loader.add_xpath(key, selector)
        yield loader.load_item()

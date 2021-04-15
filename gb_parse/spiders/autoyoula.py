import scrapy
import pymongo

class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]
    _css_selectors = {
        "brands": "div.ColumnItemList_container__5gTrc a.blackLink",
        "pagination": "div.Paginator_block__2XAPy a.Paginator_button__u1e7D",
        "car": "#serp article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu",
    }

    def _get_follow(self, response, selector_css, callback, **kwargs):
        for link_selector in response.css(selector_css):
            yield response.follow(link_selector.attrib.get("href"), callback=callback)

    def parse(self, response, **kwargs):
        yield from self._get_follow(response, self._css_selectors["brands"], self.brand_parse)

    def brand_parse(self, response):
        yield from self._get_follow(response, self._css_selectors["pagination"], self.brand_parse)
        yield from self._get_follow(response, self._css_selectors["car"], self.car_parse)

    def car_parse(self, response):
        print(1)
        data = {
            "title": response.css(".AdvertCard_advertTitle__1S1Ak::text").extract_first(),
            "url": response.url,
            "description": response.css(
                ".AdvertCard_descriptionInner__KnuRi::text"
            ).extract_first(),
            'photos': [img.attrib['src'] for img in response.css('img.PhotoGallery_photoImage__2mHGn')],
            'charateristics': dict(zip(response.css('div.AdvertSpecs_label__2JHnS::text').extract(),
                                       response.css('div.AdvertSpecs_data__xK2Qx *::text').getall()))
        }
        yield data


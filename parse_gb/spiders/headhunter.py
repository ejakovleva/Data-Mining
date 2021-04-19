import scrapy
from parse_gb.loaders_hh import HHLoader, AuthorLoader


class HeadhunterSpider(scrapy.Spider):
    name = 'headhunter'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    _xpath_selectors = {
        "pagination": "//span[contains(@class, 'bloko-button')]//a[contains(@class, 'bloko-button')]/@href",
        "vacancy": "//span[contains(@class, 'g-user-content')]//a[contains(@data-qa, 'vacancy-serp')]/@href",
        "author": "//div[contains(@class, 'vacancy-serp')]//a[contains(@href, 'employer')]/@href"
    }
    _xpath_data_query = {
        "title": "//div[@class='vacancy-title']//h1[contains(@data-qa, 'vacancy-title')]/text()",
        "salary": "//p[contains(@class, 'vacancy-salary')]//span[contains(@data-qa, 'bloko-header-2')]/text()",
        "description": '//div[@class="vacancy-description"]//text()',
        "key_qualities": "//div[@class='vacancy-section']//div[contains(@class, 'bloko-tag')]//text()",
        "author": "//a[@class='vacancy-company-name']/@href"
    }

    _xpath_author_query = {
        'title': '//span[contains(@data-qa, "title-name")]/text()',
        # 'url': '//link[@rel="canonical"]/@href',
        'activity': "//div[@class='employer-sidebar-block']//p/text()",
        'description': "//div[@data-qa='company-description-text']//div/p/text()"

    }

    def _get_follow_xpath(self, response, selector, callback, **kwargs):
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow_xpath(
            response, self._xpath_selectors["pagination"], self._parse
        )
        yield from self._get_follow_xpath(
            response, self._xpath_selectors["vacancy"], self.vacancy_parse,
        )
        yield from self._get_follow_xpath(
            response, self._xpath_selectors["author"], self.author_parse,
        )


    def vacancy_parse(self, response):
        loader = HHLoader(response=response)
        loader.add_value("url", response.url)
        for key, selector in self._xpath_data_query.items():
            loader.add_xpath(key, selector)
        yield loader.load_item()

    def author_parse(self, response):
        loader = AuthorLoader(response=response)
        loader.add_value("url", response.url)
        for key, selector in self._xpath_author_query.items():
            loader.add_xpath(key, selector)
        yield loader.load_item()

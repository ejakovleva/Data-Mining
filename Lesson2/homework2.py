import requests
from urllib.parse import urljoin
import bs4
import pymongo
import datetime


def return_date(tag, start=True):
    calendar_dict = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4, 'мая': 5, 'июн': 6, 'июл': 7, 'авг': 8, 'сен': 9,
                     'окт': 10,
                     'ноя': 11, 'дек': 12}
    promo_date = tag.find('div', attrs={'class': 'card-sale__date'}).text.split('\n')
    start_date = promo_date[1].split()
    start_date[2] = calendar_dict[start_date[2][:3]]
    start_date = datetime.date(2021, start_date[2], int(start_date[1]))
    end_date = promo_date[2].split()
    end_date[2] = calendar_dict[end_date[2][:3]]
    end_date = datetime.date(2021, end_date[2], int(end_date[1]))
    if start:
        return start_date.strftime('%m/%d/%Y')
    else:
        return end_date.strftime('%m/%d/%Y')


class MagnitParse:
    def __init__(self, start_url, db_client):
        self.start_url = start_url
        db = db_client["gb_data_mining_29_03_21"]
        self.collection = db["magnit"]

    def _get_response(self, url, *args, **kwargs):
        # TODO: Сделать Обработку ошибок и статусов
        return requests.get(url, *args, **kwargs)

    def _get_soup(self, url, *args, **kwargs):
        # TODO: Обработать ошибки
        return bs4.BeautifulSoup(self._get_response(url, *args, **kwargs).text, "lxml")

    def run(self):
        for product in self._parse(self.start_url):
            self._save(product)

    @property
    def _template(self):
        return {'url': lambda tag: urljoin(self.start_url, tag.attrs.get("href", "")),
                'promo_name': lambda tag: tag.find("div", attrs={"class": "card-sale__header"}).text,
                'product_name': lambda tag: tag.find("div", attrs={"class": "card-sale__title"}).text,
                'old_price': lambda tag: float(
                    tag.find('div', attrs={'class': 'label__price_old'}).find('span', attrs={
                        'class': 'label__price-integer'}).text + '.' + tag.find('div', attrs={
                        'class': 'label__price_old'}).find(
                        'span', attrs={'class': 'label__price-decimal'}).text),
                'new_price': lambda tag: float(
                    tag.find('div', attrs={'class': 'label__price_new'}).find('span', attrs={
                        'class': 'label__price-integer'}).text + '.' + tag.find('div', attrs={
                        'class': 'label__price_new'}).find(
                        'span', attrs={'class': 'label__price-decimal'}).text),
                'image_url': lambda tag: urljoin(self.start_url, tag.find('img', attrs={'class': 'lazy'}).attrs.get('data-src', '')),
                'date_from': lambda tag: return_date(tag, start=True),
                'date_to': lambda tag: return_date(tag, start=False)}

    def _parse(self, url):
        soup = self._get_soup(url)
        catalog_main = soup.find("div", attrs={"class": "сatalogue__main"})
        product_tags = catalog_main.find_all("a", recursive=False)
        for product_tag in product_tags:
            product = {}
            for key, funk in self._template.items():
                try:
                    product[key] = funk(product_tag)
                except (AttributeError, IndexError):
                    product[key] = ""

            yield product

    def _save(self, data):
        self.collection.insert_one(data)


if __name__ == "__main__":
    url = "https://magnit.ru/promo/"
    db_client = pymongo.MongoClient("mongodb://localhost:27017")
    parser = MagnitParse(url, db_client)
    parser.run()

"""
for itm in collection.find({'product_name': {"$regex": r".*говяд"}}, {"url":1}):
    print(itm)
"""

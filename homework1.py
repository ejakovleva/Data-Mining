import time
import json
from pathlib import Path
import requests


class Parse5ka:
    headers = {"User-Agent": "FILIPP KIRKOROV"}

    def __init__(self, start_url: str, save_path: Path):
        self.start_url = start_url
        self.save_path = save_path

    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.save_path.joinpath(f"{product['id']}.json")
            self._save(product, product_path)

    def _parse(self, url: str):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False), encoding='Utf-8')


class ParseCat5ka(Parse5ka):
    def __init__(self, start_url, save_path, cat_url):
        super().__init__(start_url, save_path)
        self.cat_url = cat_url

    def _get_categories(self):
        while True:
            response = requests.get(self.cat_url)
            if response.status_code == 200:
                categories = response.json()
                return categories
            time.sleep(0.5)

    def run(self):
        for category in self._get_categories():
            url = f'{self.start_url}?categories={category["parent_group_code"]}'
            response_cat = self._get_response(url)
            data_cat: dict = response_cat.json()
            category_path = self.save_path.joinpath(f"{category['parent_group_code']}.json")
            self._save(data_cat, category_path)



def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    cat_url = "https://5ka.ru/api/v2/categories/"
    save_path_categories = get_save_path("categories")
    cat_parser = ParseCat5ka(url, save_path_categories, cat_url)
    cat_parser.run()


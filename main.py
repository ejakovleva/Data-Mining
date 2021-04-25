
import os
import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avito_parse.spiders.autoyoula import AutoyoulaSpider
from avito_parse.spiders.instagram import InstagramSpider
from avito_parse.spiders.avito import AvitoSpider

if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    crawler_settings = Settings()
    crawler_settings.setmodule("avito_parse.settings")
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    # tags = ["python", "programming"]
    crawler_proc.crawl(
        AvitoSpider,
        # login=os.getenv("USERNAME"),
        # password=os.getenv("ENC_PASSWORD"),
        # tags=tags,
    )
    crawler_proc.start()
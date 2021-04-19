from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from parse_gb.spiders.headhunter import HeadhunterSpider


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule("parse_gb.settings")
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(HeadhunterSpider)
    crawler_proc.start()
# from scrapy.crawler import CrawlerProcess
from backend.spiders import SPIDERS
from injector import inject
from backend.services import CarInfoService
from backend.spiders.car_info_spider import CarInfoSpider


class Scraper:
    @inject
    def __init__(self, spider: CarInfoSpider, service: CarInfoService):
        self.spider = spider
        self.service = service
        self.run_spiders()

    def run_spiders(self):
        pass

        # process = CrawlerProcess({
        #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        #     'SERVICE': self.service,
        #     'LOG_LEVEL': 'INFO'
        # })
        # process.crawl(CarInfoSpider)
        # process.start()

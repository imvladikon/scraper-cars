from backend.spiders import SPIDERS
from injector import inject
from backend.services import CarInfoService
from backend.spiders.car_info_spider import CarInfoSpider


class Scraper:
    @inject
    def __init__(self, spider: CarInfoSpider, service: CarInfoService):
        self.spider = spider
        self.service = service
        # self.run_spiders()

    async def run_spiders(self, *args, **kwargs):
        await self.spider.run(*args, kwargs)

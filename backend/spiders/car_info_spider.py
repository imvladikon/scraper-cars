import logging
import os

import aiohttp
import asyncio
import types
from flask_injector import inject
from bs4 import BeautifulSoup
from typing import Iterable
from backend.services import CarInfoService
from backend.model.car_info import CarInfoDTO
from backend.utils.http import fetch, fetch_async
from backend.utils.misc import parse
from backend.utils.optional import Optional
from backend.utils.strings import blank_string
from decimal import Decimal, ROUND_UP

MAIN_URL = "https://www.classiccarsforsale.co.uk/all?page={}"
BASE_URL = "https://www.classiccarsforsale.co.uk"
pages = range(1, 75)
logger = logging.getLogger(__name__)
project_dir = os.path.dirname(os.path.realpath(__file__))


class CarInfoSpider(object):
    @inject
    def __init__(self, car_info_service: CarInfoService):
        self.car_info_service = car_info_service

    @asyncio.coroutine
    async def parse_cars(self, url) -> Iterable[CarInfoDTO]:
        async with aiohttp.ClientSession() as session:
            html = await fetch_async(session, url)
            soup = BeautifulSoup(html, 'html.parser')
            for node in soup.select(".listing"):
                yield self.parse_car(node)

    @asyncio.coroutine
    async def parse_car(self, node) -> CarInfoDTO:
        car = CarInfoDTO()
        car.phone = Optional.of(node.select_one(".fa-phone")).map(lambda e: e.text.strip()).get_or_else("")
        car.year = Optional.of(node.select_one(".listing-desc-year")).map(
            lambda e: parse(e.text.strip(), int(0))).get_or_else(0)
        car.price = Optional.of(node.select_one(".listing-desc-price")).map(
            lambda e: parse(e.text.replace("£", "").strip(), Decimal(0))).get_or_else(Decimal("0.0"))
        car.price = car.price.quantize(Decimal('0.0000'), rounding=ROUND_UP)
        car.title = Optional.of(node.select_one(".listing-desc-make-model")).map(lambda e: e.text.strip()).get_or_else(
            "")
        car.href = Optional.of(node.select_one(".listing-desc-make-model>a")).map(
            lambda e: e.get("href")).filter(blank_string).map(lambda s: f"{BASE_URL}{s.strip()}").get_or_else("")
        car.model = Optional.of(node.select_one(".listing-desc-derivative")).map(lambda e: e.text.strip()).get_or_else(
            "")
        run, gearbox, wheel_drive, refcode = Optional.of(node.select_one(".listing-desc-bullets")).map(
            lambda e: e.text.split('\n')[1:-1]).get_or_else("")
        run, gearbox, wheel_drive, refcode = run.strip(), gearbox.strip(), wheel_drive.strip(), refcode.replace(
            "Refcode:",
            "").strip()
        car.run = run
        car.gearbox = gearbox
        car.wheel_drive = wheel_drive
        car.refcode = refcode
        car.description = Optional.of(node.select_one(".listing-desc-detail")).map(
            lambda e: e.text.strip()).get_or_else("")
        logger.info(f'fetching car {car.title}')
        Optional.of(car["href"]).filter(blank_string).if_present(lambda l: self.parse_info_car(l, car))
        return car

    async def parse_info_car(self, url, car):
        async with aiohttp.ClientSession() as session:
            html = await fetch_async(session, url)
            node = BeautifulSoup(html, 'html.parser')
            car.description = (Optional.of(node.select_one(".detail-desc"))
                               .map(lambda e: e.text.strip())
                               .filter(blank_string).get_or_else(car.description))
            car.phone = Optional.of(node.select_one("label[for='phone']")).map(
                lambda e: e.text.replace("Call", "").strip()).filter(blank_string).get_or_else(car.phone)

    async def run(self, *args, **kwargs):
        cars = []
        for page in pages:
            async for car_a in await self.parse_cars(MAIN_URL.format(page)):
                car = await car_a
                cars.append(car)
                self.car_info_service.create_item(car)
            logger.info(f"fetching {page} page")
        if kwargs and "output_filename" in kwargs or "to_file" in kwargs:
            project_dir = os.path.dirname(os.path.realpath(__file__))
            output_filename = kwargs["output_filename"] or "cars.csv"
            CarInfoDTO.to_csv(cars, os.path.join(project_dir, "data", output_filename))

# -*- coding: utf-8 -*-
import click
import logging
from bs4 import BeautifulSoup
import os.path
from typing import Iterable
from utils.http import *
from models.car_info import CarInfo
from utils.optional import Optional

MAIN_URL = "https://www.classiccarsforsale.co.uk/all?page={}"
BASE_URL = "https://www.classiccarsforsale.co.uk/{}"
pages = range(1, 75)
logger = logging.getLogger(__name__)

def parse_cars(url) -> Iterable[CarInfo]:
    html = fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    return (parse_car(node) for node in soup.select(".listing"))


def parse_car(node) -> CarInfo:
    car = CarInfo()
    car.phone = Optional.of(node.select_one(".fa-phone")).map(lambda e: e.text).get_or_else("")
    car.year = Optional.of(node.select_one(".listing-desc-year")).map(lambda e: e.text).get_or_else("")
    car.price = Optional.of(node.select_one(".listing-desc-price")).map(lambda e: e.text.replace("£", "")).get_or_else("")
    car.title = Optional.of(node.select_one(".listing-desc-make-model")) .map(lambda e: e.text) .get_or_else("")
    car.href = Optional.of(node.select_one(".listing-desc-make-model>a")).map(lambda e:BASE_URL.format(e.get("href"))).get_or_else("")
    car.model = Optional.of(node.select_one(".listing-desc-derivative")).map(lambda e: e.text).get_or_else("")
    run, gearbox, wheel_drive, refcode = Optional.of(node.select_one(".listing-desc-bullets")).map(lambda e: e.text.split('\n')[1:-1]).get_or_else("")
    run, gearbox, wheel_drive, refcode = run.strip(), gearbox.strip(), wheel_drive.strip(), refcode.replace("Refcode:", "").strip()
    car.run = run
    car.gearbox = gearbox
    car.wheel_drive = wheel_drive
    car.refcode = refcode
    car.description = Optional.of(node.select_one(".listing-desc-detail")).map(lambda e: e.text).get_or_else("")
    logger.info(f'fetching car {car.title}')
    html = fetch(car["href"])
    node_page = BeautifulSoup(html, 'html.parser')
    car.description = node_page.select_one("detail-desc") or car.description
    car.phone = Optional.of(node_page.select_one("label[for='phone']")).map(lambda e: e.text.replace("Call","")).get_or_else("") or car.phone

@click.command()
@click.argument('output_filename', nargs=-1,  type=click.Path(exists=False))
def main(output_filename):
    logger = logging.getLogger(__name__)
    logger.info('start parser')
    project_dir = "."
    cars = []
    for page in pages:
        for car in parse_cars(MAIN_URL.format(page)):
            cars.append(car)
        logger.info(f"fetching {page} page")
    output_filename = output_filename or "cars.csv"
    CarInfo.to_csv(cars, os.path.join(project_dir, "data", output_filename))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()

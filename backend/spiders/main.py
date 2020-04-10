# -*- coding: utf-8 -*-
import click
from bs4 import BeautifulSoup
import os.path
from typing import Iterable
from backend.utils.http import *
from backend.model.car_info import CarInfoDTO
from backend.utils.optional import Optional
from backend.utils.strings import blank_string

MAIN_URL = "https://www.classiccarsforsale.co.uk/all?page={}"
BASE_URL = "https://www.classiccarsforsale.co.uk"
pages = range(1, 75)
logger = None
project_dir = os.path.dirname(os.path.realpath(__file__))


def parse_cars(url) -> Iterable[CarInfoDTO]:
    html = fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    return (parse_car(node) for node in soup.select(".listing"))


def parse_car(node) -> CarInfoDTO:
    car = CarInfoDTO()
    car.phone = Optional.of(node.select_one(".fa-phone")).map(lambda e: e.text.strip()).get_or_else("")
    car.year = Optional.of(node.select_one(".listing-desc-year")).map(lambda e: e.text.strip()).get_or_else("")
    car.price = Optional.of(node.select_one(".listing-desc-price")).map(
        lambda e: e.text.replace("£", "").strip()).get_or_else(
        "")
    car.title = Optional.of(node.select_one(".listing-desc-make-model")).map(lambda e: e.text.strip()).get_or_else("")
    car.href = Optional.of(node.select_one(".listing-desc-make-model>a")).map(
        lambda e: e.get("href")).filter(blank_string).map(lambda s: f"{BASE_URL}{s.strip()}").get_or_else("")
    car.model = Optional.of(node.select_one(".listing-desc-derivative")).map(lambda e: e.text.strip()).get_or_else("")
    run, gearbox, wheel_drive, refcode = Optional.of(node.select_one(".listing-desc-bullets")).map(
        lambda e: e.text.split('\n')[1:-1]).get_or_else("")
    run, gearbox, wheel_drive, refcode = run.strip(), gearbox.strip(), wheel_drive.strip(), refcode.replace("Refcode:",
                                                                                                            "").strip()
    car.run = run
    car.gearbox = gearbox
    car.wheel_drive = wheel_drive
    car.refcode = refcode
    car.description = Optional.of(node.select_one(".listing-desc-detail")).map(lambda e: e.text.strip()).get_or_else("")
    logger.info(f'fetching car {car.title}')
    Optional.of(car["href"]).filter(blank_string).if_present(lambda l: parse_info_car(l, car))
    return car


def parse_info_car(url, car):
    html = fetch(url)
    node = BeautifulSoup(html, 'html.parser')
    car.description = Optional.of(node.select_one(".detail-desc")) \
        .map(lambda e: e.text.strip()) \
        .filter(blank_string) \
        .get_or_else(car.description)
    car.phone = Optional.of(node.select_one("label[for='phone']")).map(
        lambda e: e.text.replace("Call", "").strip()).filter(blank_string).get_or_else(car.phone)


@click.command()
@click.argument('output_filename', nargs=-1, type=click.Path(exists=False))
def main(output_filename):
    logger.info('start parser')
    project_dir = os.path.dirname(os.path.realpath(__file__))
    cars = []
    for page in pages:
        for car in parse_cars(MAIN_URL.format(page)):
            cars.append(car)
        logger.info(f"fetching {page} page")
    output_filename = output_filename or "cars.csv"
    CarInfoDTO.to_csv(cars, os.path.join(project_dir, "data", output_filename))


def create_logger():
    import time
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    fh = logging.FileHandler(os.path.join(project_dir, "logs", f"{time.strftime('%H_%M_%b_%d_%Y')}.log"))
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    # logger = create_logger()
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()

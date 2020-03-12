# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import os.path
import aiohttp
import asyncio
from typing import List, Iterable

from models.car_info import CarInfo
from utils.optional import Optional

BASE_URL = "https://www.classiccarsforsale.co.uk/all?page={}"
pages = range(1, 75)


def parse_cars(url) -> Iterable[CarInfo]:
    html = fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    return (parse_car(node) for node in soup.select(".listing"))


def parse_car(node) -> CarInfo:
    dict = {}
    dict["phone"] = Optional.of(node.select_one(".fa-phone")) \
        .map(lambda e: e.text) \
        .get_or_else("")
    dict["year"] = Optional \
        .of(node.select_one(".listing-desc-year")) \
        .map(lambda e: e.text) \
        .get_or_else("")
    dict["price"] = Optional \
        .of(node.select_one(".listing-desc-price")) \
        .map(lambda e: e.text.replace("£", "")) \
        .get_or_else("")
    dict["title"] = Optional \
        .of(node.select_one(".listing-desc-make-model")) \
        .map(lambda e: e.text.replace("£", "")) \
        .get_or_else("")
    dict["model"] = Optional \
        .of(node.select_one(".listing-desc-derivative")) \
        .map(lambda e: e.text.replace("£", "")) \
        .get_or_else("")
    run, gearbox, wheel_drive, refcode = Optional \
        .of(node.select_one(".listing-desc-bullets")) \
        .map(lambda e: e.text.split('\n')[1:-1]) \
        .get_or_else("")
    run, gearbox, wheel_drive, refcode = run.strip(), gearbox.strip(), wheel_drive.strip(), refcode.replace("Refcode:",
                                                                                                            "").strip()
    dict["run"] = run
    dict["gearbox"] = gearbox
    dict["wheel_drive"] = wheel_drive
    dict["refcode"] = refcode
    dict["description"] = node.select_one(".listing-desc-detail").text
    return CarInfo(dict)


def fetch(url):
    page = requests.get(url)
    page.encoding = page.apparent_encoding
    return page.text


def main():
    logger = logging.getLogger(__name__)
    logger.info('start parser')
    project_dir = "."
    cars = []
    for page in pages:
        for car in parse_cars(BASE_URL.format(page)):
            cars.append(car)
        logger.info(f"fetching {page} page")
    CarInfo.to_csv(cars, os.path.join(project_dir, "data", "cars.csv"))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()

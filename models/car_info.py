import logging
from enum import Enum
import csv
from typing import List


class Gearbox(Enum):
    Manual = 1,
    Auto = 2


class CarInfo(dict):

    __slots__ = ("title", "model", "year", "run", "gearbox", "wheel_drive", "refcode", "phone", "price", "description")

    def __init__(self, info: dict = None):
        if not info:
            return
        for key, value in info.items():
            setattr(self, key, value)

    def __str__(self):
        return f"{self.title} {self.model} {self.price}"

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            logger = logging.getLogger(__name__)
            logger.error(e)

    def __setattr__(self, name, value):
        try:
            self[name] = value
        except KeyError as e:
            logger = logging.getLogger(__name__)
            logger.error(e)

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError as e:
            logger = logging.getLogger(__name__)
            logger.error(e)

    @staticmethod
    def get_fields():
        return {"title", "model", "year", "run", "gearbox", "wheel_drive", "refcode", "phone", "price", "description"}

    @staticmethod
    def to_csv(cars: List[dict], filename: str):
        with open(filename, "w") as f:
            wr = csv.DictWriter(f, delimiter="\t", fieldnames=list(CarInfo.get_fields()))
            wr.writeheader()
            wr.writerows(cars)

import logging
from enum import Enum
import csv
from typing import List
from app.utils.misc import exception
import pickle

logger = logging.getLogger(__name__)


class Gearbox(Enum):
    Manual = 1,
    Auto = 2


class CarInfo(dict):
    __slots__ = (
        "title", "model", "year", "run", "gearbox", "wheel_drive", "refcode", "phone", "price", "description", "href")

    def __init__(self, info: dict = None):
        if not info:
            return
        for key, value in info.items():
            setattr(self, key, value)

    def __str__(self):
        return f"{self.title} {self.model} {self.price}"

    @exception(logger, reraise=False)
    def __getattr__(self, name):
        return self[name]

    @exception(logger, reraise=False)
    def __setattr__(self, name, value):
        self[name] = value

    @exception(logger, reraise=False)
    def __delattr__(self, name):
        del self[name]

    @staticmethod
    def get_fields():
        return {"title", "model", "year", "run", "gearbox", "wheel_drive", "refcode", "phone", "price", "description",
                "href"}

    @staticmethod
    @exception(logger, reraise=False)
    def to_csv(cars: List[dict], filename: str):
        with open(filename, "w") as f:
            wr = csv.DictWriter(f, delimiter="\t", fieldnames=list(CarInfo.get_fields()))
            wr.writeheader()
            wr.writerows(cars)

    @staticmethod
    @exception(logger, reraise=False)
    def to_pickle(cars: List[dict], filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(cars, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    @exception(logger, reraise=False)
    def from_pickle(filename: str) -> List[dict]:
        with open(filename, 'rb') as f:
            return pickle.load(f)

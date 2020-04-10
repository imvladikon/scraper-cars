import json

from pony.orm import *
from pony.orm import Database as PonyDatabase
from decimal import Decimal

from backend.model.car_info import CarInfoDTO


class DB:

    def __init__(self, **db_params):
        self.model = PonyDatabase(**db_params)

        class CarInfo(self.model.Entity):
            __json_fields__ = ("id",
                         "title", "model", "year", "run", "gearbox", "wheel_drive", "refcode", "phone", "price",
                         "description",
                         "href")

            id = PrimaryKey(int, auto=True)
            title = Optional(str, nullable=True)
            model = Optional(str, nullable=True)
            year = Optional(int, nullable=True)
            run = Optional(str, nullable=True)
            gearbox = Set('Gearbox', cascade_delete=False)
            wheel_drive = Optional(str, nullable=True)
            refcode = Optional(str, nullable=True)
            phone = Optional(str, nullable=True)
            price = Optional(Decimal)
            description = Optional(str, nullable=True)
            href = Optional(str, nullable=True)

        class Gearbox(self.model.Entity):
            code = Required(int)
            title = Required(str)
            owner = Required(CarInfo)

            def as_json(self):
                return json.dumps(self, default=lambda o: o.__dict__,
                                  sort_keys=True, indent=4)

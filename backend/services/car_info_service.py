from flask_injector import inject
from pony.orm import db_session
from backend.model.entities import Database

class CarInfoService:
    @inject
    def __init__(self, db: Database):
        self.db = db

    @db_session
    def find_by_id(self, id):
        entry = self.db.model.CarInfo[id]
        if entry is None:
            car_info = self.db.model.CarInfo()
            return car_info.to_dict()
        return entry.to_dict()

    @db_session
    def find_by_title(self, title):
        entry = self.db.model.CarInfo.get(lambda s: s.title == title)
        if entry is None:
            car_info = self.db.model.CarInfo(title=title)
            return car_info.to_dict()
        return entry.to_dict()

    @db_session
    def list(self):
        car_infos = self.db.model.CarInfo.select()
        car_info_list = [car_info.to_dict() for car_info in car_infos]
        return car_info_list
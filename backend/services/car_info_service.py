from flask_injector import inject
from pony.orm import db_session

from backend.model.car_info import CarInfoDTO
from backend.model.entities import DB


class CarInfoService:
    @inject
    def __init__(self, db: DB):
        self.db = db

    @db_session
    def find_by_id(self, id):
        assert id
        entry = self.db.model.CarInfo[id]
        if entry:
            return entry.to_dict()
        return {"message": "Car-info not found."}, 404

    @db_session
    def find_by_href(self, href):
        assert href
        entry = self.db.model.CarInfo.get(lambda s: s.href == href)
        if entry:
            return entry.to_dict()
        return {"message": "Car-info not found."}, 404

    @db_session
    def find_by_title(self, title):
        assert title
        entry = self.db.model.CarInfo.get(lambda s: s.title == title)
        if entry is None:
            car_info = self.db.model.CarInfo(title=title)
            return car_info.to_dict()
        return entry.to_dict()

    @db_session
    def create_item(self, *args, **kwargs):
        dto = None
        if args and isinstance(args[0], (CarInfoDTO, dict)):
            dto = args[0]
        elif kwargs:
            dto = kwargs
        entry = None
        if "href" in dto:
            entry = self.db.model.CarInfo.get(lambda s: s.href == dto.get("href", ""))
        if dto and entry is None:
            del dto["gearbox"]
            #TODO: add gearbox mapping and saving
            return self.db.model.CarInfo(**args[0]).to_dict()
        return None

    @db_session
    def list(self):
        car_infos = self.db.model.CarInfo.select()
        car_info_list = [car_info.to_dict() for car_info in car_infos]
        return car_info_list

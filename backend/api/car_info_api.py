from flask import jsonify
from flask_restful import Resource, reqparse
from flask_injector import inject

from backend.services import CarInfoService


class CarInfo(Resource):
    ENDPOINT = "/api/v1/resources/cars/<int:entry_id>"

    @inject
    def __init__(self, car_info_service: CarInfoService):
        self.car_info_service = car_info_service

        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "price",
            type=float,
            required=True,
            help="The \"price\" field cannot be left blank!"
        )
        self.parser.add_argument(
            "store_id",
            type=str,
            required=True,
            help="Cannot insert item without a store ID!"
        )

    def get(self, entry_id):
        return self.car_info_service.find_by_id(entry_id)


class CarInfoList(Resource):
    ENDPOINT = "/api/v1/resources/cars/all"

    @inject
    def __init__(self, car_info_service: CarInfoService):
        self.car_info_service = car_info_service

    def get(self):
        return self.car_info_service.list()

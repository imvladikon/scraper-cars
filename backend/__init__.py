from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector, request
from pony.orm import Database
from injector import Module, Injector, inject, singleton
from backend.config import config
from pony.flask import Pony

from backend.model.entities import DB
from backend.services import SERVICES, CarInfoService

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(config)
Pony(app)
CORS(app, resources=r'/*', allow_headers="Content-Type")
db = DB()


def configure(binder):
    # db = Database(**args)
    # db.model.generate_mapping(create_tables=True)
    binder.bind(Database, to=db, scope=request)
    for service in SERVICES:
        binder.bind(service, scope=request)
    # binder.bind(CarInfoService, to=car_info_service, scope=request)


FlaskInjector(app=app, modules=[configure])

import backend.views

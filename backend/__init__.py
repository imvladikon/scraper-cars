from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_injector import FlaskInjector, request
from injector import singleton

from backend.api import API_HANDLERS
from backend.config import config
from pony.flask import Pony

from backend.model.entities import DB
from backend.services import SERVICES, CarInfoService

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(config)
Pony(app)
CORS(app, resources=r'/*', allow_headers="Content-Type")
api = Api(app=app)

for handler in API_HANDLERS:
    api.add_resource(handler, handler.ENDPOINT)


def configure(binder):
    for service in SERVICES:
        binder.bind(service, scope=request)
    db = DB(**app.config['PONY'])
    db.model.generate_mapping(create_tables=True)
    binder.bind(DB, to=db, scope=singleton)
    for service in SERVICES:
        binder.bind(service, scope=singleton)


injector = FlaskInjector(app=app, modules=[configure])


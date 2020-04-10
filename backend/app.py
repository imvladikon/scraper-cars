from flask_injector import singleton
from injector import Injector
from pony.orm import Database

from backend import db
from backend.scrape import Scraper
from backend.services import SERVICES
from backend.spiders import SPIDERS
import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

def configure(binder):
    # db = Database(**args)
    # db.model.generate_mapping(create_tables=True)
    binder.bind(Database, to=db, scope=singleton)
    for service in SERVICES:
        binder.bind(service, scope=singleton)
    for spider in SPIDERS:
        binder.bind(spider)

injector = Injector(modules=[configure])


if __name__ == "__main__":
    scraper = injector.get(Scraper)
   # for service in SERVICES:
   #     service.get_list()

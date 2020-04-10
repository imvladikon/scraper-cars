from backend import app, db, CarInfoService

from flask import jsonify, request, url_for, render_template, flash, redirect, abort
from flask import json
from pony.orm import flush

from backend.utils.error_handlers import InvalidUsage

@app.route("/api/v1/resources/cars/all", methods=["GET"])
def get_cars():
    car_infos = db.model.CarInfo.select()
    return jsonify(list(car_infos))

@app.route("/api/v1/resources/cars/<int:entry_id>", methods=["GET"])
def get_car(entry_id, service:CarInfoService):
    entry = db.model.CarInfo[entry_id]
    entry2 = service.find_by_id(entry_id)
    return jsonify(entry.to_dict())

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def construct_dict(entry):
    if entry.order:
        return dict(title=entry.title, completed=entry.completed,
                    url=url_for("entry", entry_id=entry.id, _external=True),
                    order=entry.order)
    else:
        return dict(title=entry.title, completed=entry.completed,
                    url=url_for("entry", entry_id=entry.id, _external=True))


@app.teardown_appcontext
def shutdown_session(exception=None):
    pass
    # db_session.remove()

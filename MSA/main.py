import time 
import base64
import os
import json
from functools import wraps
import requests
import logging
import sys
import urllib
from flask import Flask, request, jsonify, make_response, abort, url_for
from flask_restful import reqparse, abort, Api, Resource

time.sleep(20)

from data import *

from controllers.drivers import Driver, DriverList
from controllers.cars import Car, CarList
from controllers.trips import Trip, TripList
from controllers.car_drivers import CarDriver, CarDriverList

app = Flask(__name__)
api = Api(app)

@app.before_request
def check_authorization():
  try:
    input = json.dumps({
      "method": request.method,
      "path": request.path.strip().split("/")[1:],
      "user": get_authentication(request),
    }, indent=2)
    url = os.environ.get("OPA_URL", "http://opa:8181")
    app.logger.debug("OPA query: %s. Body: %s", url, input)
    response = requests.post(url, data=input)
  except Exception as e:
    app.logger.exception("Unexpected error querying OPA.")
    abort(500)

  if response.status_code != 200:
    app.logger.error("OPA status code: %s. Body: %s",
                      response.status_code, response.json())
    abort(500)

  allowed = response.json()
  app.logger.debug("OPA result: %s", allowed)
  if not allowed:
    abort(403)


def get_authentication(request):
  return request.headers.get("Authorization", "")

## Routing
api.add_resource(DriverList,    '/drivers')
api.add_resource(Driver,        '/drivers/<int:driver_id>')
api.add_resource(CarList,       '/cars')
api.add_resource(Car,           '/cars/<int:car_id>')
api.add_resource(TripList,      '/trips')
api.add_resource(Trip,          '/trips/<int:trip_id>')
api.add_resource(CarDriverList, '/car_drivers')
api.add_resource(CarDriver,     '/car_drivers/<int:car_driver_id>')

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import time 
time.sleep(20)

from data import *

from controllers.drivers import Driver, DriverList
from controllers.cars import Car, CarList
from controllers.trips import Trip, TripList
from controllers.car_drivers import CarDriver, CarDriverList

app = Flask(__name__)
api = Api(app)

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
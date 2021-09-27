from flask_restful import Resource, abort, reqparse
from data import DRIVERS
from services.producer import send_message_to_kafka

driver_parser = reqparse.RequestParser()
driver_parser.add_argument('name')

class DriverList(Resource):
  def get(self):
    return DRIVERS

  def post(self):
    args = driver_parser.parse_args()
    driver_id = self.generate_id()
    new_driver = {'id': driver_id, 'name': args['name']}
    DRIVERS.append(new_driver)
    send_message_to_kafka('drivers', {**new_driver, **{'state': 'created'}})
    return self.get_driver(driver_id), 201
  
  def generate_id(self):
    return max([ int(item['id']) for item in DRIVERS ]) + 1

  def get_driver(self, driver_id):
    return next((item for item in DRIVERS if int(item["id"]) == int(driver_id)), None)

class Driver(Resource):
  def get(self, driver_id):
    driver = self.get_driver(driver_id)
    self.abort_if_driver_doesnt_exist(driver_id, driver)
    return driver

  def delete(self, driver_id):
    driver = self.get_driver(driver_id)
    self.abort_if_driver_doesnt_exist(driver_id, driver)
    DRIVERS[:] = [d for d in DRIVERS if int(d.get('id')) != int(driver_id)]
    send_message_to_kafka('drivers', {**driver, **{'state': 'deleted'}})
    return 'Deleted successfully', 204

  def put(self, driver_id):
    existing_driver = self.get_driver(driver_id)
    self.abort_if_driver_doesnt_exist(driver_id, existing_driver)
    args = driver_parser.parse_args()
    DRIVERS[:] = [d for d in DRIVERS if int(d.get('id')) != int(driver_id)]
    new_driver = {'id': driver_id, 'name': args['name']}
    DRIVERS.append(new_driver)
    DRIVERS[:] = sorted(DRIVERS, key = lambda i: int(i['id']))
    send_message_to_kafka('drivers', {**new_driver, **{'state': 'updated'}})
    return new_driver, 201

  def get_driver(self, driver_id):
    return next((item for item in DRIVERS if int(item["id"]) == int(driver_id)), None)

  def abort_if_driver_doesnt_exist(self, driver_id, driver):
    if driver == None:
      abort(404, message="Driver {} doesn't exist".format(driver_id))
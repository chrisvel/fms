from flask_restful import Resource, abort, reqparse
from data import CAR_DRIVERS
from services.producer import send_message_to_kafka

car_driver_parser = reqparse.RequestParser()
car_driver_parser.add_argument('car_id')
car_driver_parser.add_argument('driver_id')

class CarDriverList(Resource):
  def get(self):
    return CAR_DRIVERS

  def post(self):
    args = car_driver_parser.parse_args()
    car_driver_id = self.__generate_id()
    new_car_driver = {'id': car_driver_id, 'car_id': str(args['car_id']), 'driver_id': str(args['driver_id'])}
    CAR_DRIVERS.append(new_car_driver)
    send_message_to_kafka('car_drivers', {**new_car_driver, **{'state': 'created'}})
    return self.__set_car_driver(car_driver_id), 201
  
  def __generate_id(self):
    return max([ int(item['id']) for item in CAR_DRIVERS ]) + 1

  def __set_car_driver(self, car_driver_id):
    return next((item for item in CAR_DRIVERS if int(item["id"]) == int(car_driver_id)), None)
class CarDriver(Resource):
  def get(self, car_driver_id):
    car_driver = self.__set_car_driver(car_driver_id)
    self.__abort_if_car_driver_doesnt_exist(car_driver_id, car_driver)
    return car_driver

  def delete(self, car_driver_id):
    car_driver = self.__set_car_driver(car_driver_id)
    self.__abort_if_car_driver_doesnt_exist(car_driver_id, car_driver)
    CAR_DRIVERS[:] = [d for d in CAR_DRIVERS if int(d.get('id')) != int(car_driver_id)]
    send_message_to_kafka('car_drivers', {**car_driver, **{'state': 'deleted'}})
    return 'Deleted successfully', 204

  def put(self, car_driver_id):
    existing_car_driver = self.__set_car_driver(car_driver_id)
    self.__abort_if_car_driver_doesnt_exist(car_driver_id, existing_car_driver)
    args = car_driver_parser.parse_args()
    CAR_DRIVERS[:] = [d for d in CAR_DRIVERS if int(d.get('id')) != int(car_driver_id)]
    new_car_driver = {'id': car_driver_id, 'car_id': str(args['car_id']), 'driver_id': str(args['driver_id'])}
    CAR_DRIVERS.append(new_car_driver)
    CAR_DRIVERS[:] = sorted(CAR_DRIVERS, key = lambda i: int(i['id']))
    send_message_to_kafka('car_drivers', {**new_car_driver, **{'state': 'updated'}})
    return new_car_driver, 201

  def __set_car_driver(self, car_driver_id):
    return next((item for item in CAR_DRIVERS if int(item["id"]) == int(car_driver_id)), None)

  def __abort_if_car_driver_doesnt_exist(self, car_driver_id, car_driver):
    if car_driver == None:
      abort(404, error="CarDriver {} doesn't exist".format(car_driver_id))
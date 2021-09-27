from flask_restful import Resource, abort, reqparse
from data import CARS
from services.producer import send_message_to_kafka

car_parser = reqparse.RequestParser()
car_parser.add_argument('model')

class CarList(Resource):
  def get(self):
    return CARS

  def post(self):
    args = car_parser.parse_args()
    car_id = self.generate_id()
    new_car = {'id': car_id, 'model': args['model']}
    CARS.append(new_car)
    send_message_to_kafka('cars', {**new_car, **{'state': 'created'}})
    return self.get_car(car_id), 201
  
  def generate_id(self):
    return max([ int(item['id']) for item in CARS ]) + 1

  def get_car(self, car_id):
    return next((item for item in CARS if int(item["id"]) == int(car_id)), None)

class Car(Resource):
  def get(self, car_id):
    car = self.get_car(car_id)
    self.abort_if_car_doesnt_exist(car_id, car)
    return car

  def delete(self, car_id):
    car = self.get_car(car_id)
    self.abort_if_car_doesnt_exist(car_id, car)
    CARS[:] = [d for d in CARS if int(d.get('id')) != int(car_id)]
    send_message_to_kafka('cars', {**car, **{'state': 'deleted'}})
    return 'Deleted successfully', 204

  def put(self, car_id):
    existing_car = self.get_car(car_id)
    self.abort_if_car_doesnt_exist(car_id, existing_car)
    args = car_parser.parse_args()
    CARS[:] = [d for d in CARS if int(d.get('id')) != int(car_id)]
    new_car = {'id': car_id, 'model': args['model']}
    CARS.append(new_car)
    CARS[:] = sorted(CARS, key = lambda i: int(i['id']))
    send_message_to_kafka('cars', {**new_car, **{'state': 'updated'}})
    return new_car, 201

  def get_car(self, car_id):
    return next((item for item in CARS if int(item["id"]) == int(car_id)), None)

  def abort_if_car_doesnt_exist(self, car_id, car):
    if car == None:
      abort(404, message="Car {} doesn't exist".format(car_id))
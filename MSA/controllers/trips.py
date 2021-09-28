from flask_restful import Resource, abort, reqparse
from data import TRIPS
from services.producer import send_message_to_kafka

trip_parser = reqparse.RequestParser()
trip_parser.add_argument('from_location')
trip_parser.add_argument('to_location')

class TripList(Resource):
  def get(self):
    return TRIPS

  def post(self):
    args = trip_parser.parse_args()
    trip_id = self.__generate_id()
    new_trip = {'id': trip_id, 'from_location': args['from_location'], 'to_location': args['to_location']}
    TRIPS.append(new_trip)
    send_message_to_kafka('trips', {**new_trip, **{'state': 'created'}})
    return self.__set_trip(trip_id), 201
  
  def __generate_id(self):
    return max([ int(item['id']) for item in TRIPS ]) + 1

  def __set_trip(self, trip_id):
    return next((item for item in TRIPS if int(item["id"]) == int(trip_id)), None)

class Trip(Resource):
  def get(self, trip_id):
    trip = self.__set_trip(trip_id)
    self.__abort_if_trip_doesnt_exist(trip_id, trip)
    return trip

  def delete(self, trip_id):
    trip = self.__set_trip(trip_id)
    self.__abort_if_trip_doesnt_exist(trip_id, trip)
    TRIPS[:] = [d for d in TRIPS if int(d.get('id')) != int(trip_id)]
    send_message_to_kafka('trips', {**trip, **{'state': 'deleted'}})
    return 'Deleted successfully', 204

  def put(self, trip_id):
    existing_trip = self.__set_trip(trip_id)
    self.__abort_if_trip_doesnt_exist(trip_id, existing_trip)
    args = trip_parser.parse_args()
    TRIPS[:] = [d for d in TRIPS if int(d.get('id')) != int(trip_id)]
    new_trip = {'id': trip_id, 'from_location': args['from_location'], 'to_location': args['to_location']}
    TRIPS.append(new_trip)
    TRIPS[:] = sorted(TRIPS, key = lambda i: int(i['id']))
    send_message_to_kafka('trips', {**new_trip, **{'state': 'updated'}})
    return new_trip, 201

  def __set_trip(self, trip_id):
    return next((item for item in TRIPS if int(item["id"]) == int(trip_id)), None)

  def __abort_if_trip_doesnt_exist(self, trip_id, trip):
    if trip == None:
      abort(404, error="Trip {} doesn't exist".format(trip_id))
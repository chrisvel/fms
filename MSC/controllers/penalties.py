from flask_restful import Resource, abort, reqparse

from operator import itemgetter

from tinydb import TinyDB, Query
db = TinyDB('db.json')

class PenaltyList(Resource):
  def get(self):
    penalties = db.all()
    return sorted(penalties, key=itemgetter('driver_id')) 
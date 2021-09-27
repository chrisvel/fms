from kafka import KafkaProducer, KafkaConsumer
from services.penalty import calc_penalty_score
import json
import os

from tinydb import TinyDB, Query, where
db = TinyDB('db.json')

def consume_messages_from_kafka():
  # try:
    print('Starting consumer', flush=True)
    consumer = KafkaConsumer(
      'car_states', 
      bootstrap_servers=[os.environ.get('BOOTSTRAP_SERVERS')], 
      value_deserializer=lambda m: json.loads(m))
    for message in consumer:
      car_state = message.value
      if int(car_state['speed']) > 60:
        penalty_score = calc_penalty_score(car_state)
        drivers = db.search(where('driver_id') == str(car_state['driver_id']))
        if drivers== []:
          db.insert({'driver_id': car_state['driver_id'], 'penalty': str(penalty_score)})
        else: 
          old_score = int(drivers[0]['penalty'])
          new_score = old_score + penalty_score
          speed = car_state['speed']
          db.update({'penalty': str(new_score)}, where('driver_id') == str(car_state['driver_id']))
          print(f'speed: {speed} -- old_score: {old_score} ---- additional score: {penalty_score} ---- new score: {new_score}', flush=True)
  # except:
  #   print("Error!!")
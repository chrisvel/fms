from services.kafka import send_message_to_kafka
import time
import random 

HEARTBEAT_INTERVAL = 3

def generate_heartbeat(data, locks):
  while True:
    generate_random_trip(data)
    time.sleep(HEARTBEAT_INTERVAL)

def generate_random_trip(data):
  car_drivers = data['car_drivers']
  if car_drivers == []:
    print('No cars assigned to drivers', flush=True)
  else:
    random_car_driver = random.choice(car_drivers)
    random_speed = random.randint(0, 200)
    random_location_spot = [random.uniform(-180,180), random.uniform(-90, 90)]

    payload = {
      'car_id': random_car_driver["car_id"],
      'driver_id': random_car_driver["driver_id"],
      'speed': random_speed,
      'coords': random_location_spot
    }
  
    send_message_to_kafka('car_states', payload)
    print(payload, flush=True)


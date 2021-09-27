from services.kafka import consume_messages_from_kafka
from services.simulator import generate_heartbeat
import threading
import time 
time.sleep(20)

data = {
  'drivers': [],
  'cars': [],
  'trips': [],
  'car_drivers': []
}

locks = {
  'drivers': threading.Lock(),
  'cars': threading.Lock(),
  'trips': threading.Lock(),
  'car_drivers': threading.Lock()
}

print('Starting Kafka listeners')

consumer1_thread = threading.Thread(target=consume_messages_from_kafka, args=['drivers', data, locks])
consumer2_thread = threading.Thread(target=consume_messages_from_kafka, args=['cars', data, locks])
consumer3_thread = threading.Thread(target=consume_messages_from_kafka, args=['trips', data, locks])
consumer4_thread = threading.Thread(target=consume_messages_from_kafka, args=['car_drivers', data, locks])

consumer1_thread.start()
consumer2_thread.start()
consumer3_thread.start()
consumer4_thread.start()

print ('Starting trip randomizer')

trip_randomizer = threading.Thread(target=generate_heartbeat, args=[data, locks])
trip_randomizer.start()
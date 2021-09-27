import os 
import requests
from faker import Faker
from faker_vehicle import VehicleProvider

def create_topics():
  command = 'docker-compose exec kafka kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic'
  print('--| Creating kafka topics: ')
  os.system(f'{command} drivers')
  os.system(f'{command} cars')
  os.system(f'{command} trips')
  os.system(f'{command} car_drivers')
  os.system(f'{command} car_states')
  print('\n')

def create_drivers():
  print('--| Creating fake drivers: ')
  fake = Faker()
  post_url = 'http://localhost:5000/drivers'
  for _ in range(50):
    random_name = fake.name()
    print(f'------| Creating driver with name [{random_name}]')
    requests.post(post_url, data={'name': random_name})
  print('\n')

def create_cars():
  print('--| Creating fake cars: ')
  fake = Faker()
  fake.add_provider(VehicleProvider)
  post_url = 'http://localhost:5000/cars'
  for _ in range(50):
    random_model = fake.vehicle_year_make_model()
    print(f'------| Creating car with model [{random_model}]')
    requests.post(post_url, data={'model': random_model})
  print('\n')

def create_trips():
  print('--| Creating fake trips: ')
  fake = Faker()
  post_url = 'http://localhost:5000/trips'
  for _ in range(50):
    random_trip_from = fake.address().replace('\n',', ')
    random_trip_to = fake.address().replace('\n',', ')
    print(f'------| Creating trip with data [{random_trip_from}] > [{random_trip_to}]')
    requests.post(post_url, data={'from_location': random_trip_from, 'to_location': random_trip_to})
  print('\n')

def create_car_drivers():
  print('--| Creating fake car_drivers: ')
  post_url = 'http://localhost:5000/car_drivers'
  for driver_id in range(8):
    car_id = 8 - (driver_id)
    print(f'------| Creating car_driver with ids [{driver_id + 1} <=> {car_id}]')
    requests.post(post_url, data={'driver_id': driver_id + 1, 'car_id': car_id})
  print('\n')

def clean_up_penalties_db():
  print('--| Cleaning up penalties DB ')
  with open('MSC/db.json', "w") as dbfile:
    dbfile.write('{}')
  print('\n')

# create_topics()
clean_up_penalties_db()
create_drivers()
create_cars()
create_trips()
create_car_drivers()
print('--| DONE |--')
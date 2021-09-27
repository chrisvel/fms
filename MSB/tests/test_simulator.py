import pytest
from unittest import mock

from services.simulator import generate_random_trip
from services.kafka import send_message_to_kafka

def test_simulator_produces_message():
  topic = 'car_states'
  data = {
    'car_drivers': [{'id': '11', 'car_id': '21', 'driver_id': '12'}]
  }
  with mock.patch('services.simulator.send_message_to_kafka', return_value=True) as smtk:
    generate_random_trip(data)
    smtk.assert_called_once()

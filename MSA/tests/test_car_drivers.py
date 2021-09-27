import os
import pytest
from unittest import mock

from flask import json
from services.producer import send_message_to_kafka

from main import app
from data import *

@pytest.fixture
def client(request):
  test_client = app.test_client()
  
  def teardown():
      pass 

  request.addfinalizer(teardown)
  return test_client

def load_json_response(response):
  return json.loads(response.data.decode('utf8'))

def test_get_car_driver(client):
  response = client.get('/car_drivers/1')
  expected_data = next(item for item in CAR_DRIVERS if item["id"] == "1")
  assert response.content_type == 'application/json'
  assert response.status_code == 200
  assert load_json_response(response) == expected_data

def test_get_car_drivers(client):
  response = client.get('/car_drivers')
  assert response.content_type == 'application/json'
  assert response.status_code == 200
  assert load_json_response(response) == CAR_DRIVERS

def test_post_car_drivers(client):
  data = {"car_id": "1", "driver_id": "2"}
  with mock.patch('controllers.car_drivers.send_message_to_kafka', return_value=True) as smtk:
    response = client.post('/car_drivers', data=data)
    expected_id = len(CAR_DRIVERS)
    smtk.assert_called_once()
    assert response.content_type == 'application/json'
    assert response.status_code == 201
    assert load_json_response(response) == {'id': expected_id, "car_id": "1", "driver_id": "2"}
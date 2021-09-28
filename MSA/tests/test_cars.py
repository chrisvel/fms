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

def test_get_car(client):
  response = client.get('/cars/1')
  expected_data = next(item for item in CARS if item["id"] == "1")
  assert response.content_type == 'application/json'
  assert response.status_code == 200
  assert load_json_response(response) == expected_data

def test_get_car_not_exists(client):
  response = client.get('/cars/13')
  expected_data = {'error': "Car 13 doesn't exist"}
  assert response.content_type == 'application/json'
  assert response.status_code == 404
  assert load_json_response(response) == expected_data

def test_get_car_wrong_type_params(client):
  response = client.get('/cars/abc')
  assert response.status_code == 404

def test_get_cars(client):
  response = client.get('/cars')
  assert response.content_type == 'application/json'
  assert response.status_code == 200
  assert load_json_response(response) == CARS

def test_post_cars(client):
  data = {'model': '2020 Toyota Avensis'}
  with mock.patch('controllers.cars.send_message_to_kafka', return_value=True) as smtk:
    response = client.post('/cars', data=data)
    expected_id = len(CARS)
    smtk.assert_called_once()
    assert response.content_type == 'application/json'
    assert response.status_code == 201
    assert load_json_response(response) == {'id': expected_id, 'model': data['model']}

def test_put_cars(client):
  data = {'model': '2020 Toyota Yaris'}
  with mock.patch('controllers.cars.send_message_to_kafka', return_value=True) as smtk:
    response = client.put('/cars/1', data={'model': data["model"]})
    smtk.assert_called_once()
    assert response.content_type == 'application/json'
    assert response.status_code == 201
    assert load_json_response(response) == {'id': 1, 'model': data['model']}

def test_delete_car(client):
  data = CARS[0]
  cars_len = len(CARS)
  with mock.patch('controllers.cars.send_message_to_kafka', return_value=True) as smtk:
    response = client.delete('/cars/1')
    expected_cars = cars_len - 1
    smtk.assert_called_once()
    assert response.content_type == 'application/json'
    assert response.status_code == 204
    assert expected_cars == len(CARS)
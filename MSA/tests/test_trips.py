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

def test_get_trip(client):
  response = client.get('/trips/1')
  expected_data = next(item for item in TRIPS if item["id"] == "1")
  assert response.content_type == 'application/json'
  assert response.status_code == 200
  assert load_json_response(response) == expected_data

def test_get_driver_not_exists(client):
  response = client.get('/trips/132')
  expected_data = {'error': "Trip 132 doesn't exist"}
  assert response.content_type == 'application/json'
  assert response.status_code == 404
  assert load_json_response(response) == expected_data

def test_get_driver_wrong_type_params(client):
  response = client.get('/trips/abc')
  assert response.status_code == 404

def test_get_trips(client):
  response = client.get('/trips')
  assert response.content_type == 'application/json'
  assert response.status_code == 200
  assert load_json_response(response) == TRIPS

def test_post_trips(client):
  data = {"from_location": "111 Syggrou avenue, Athens, Greece", "to_location": "512 Vouliagmenis avenue, Voula, Greece"}
  with mock.patch('controllers.trips.send_message_to_kafka', return_value=True) as smtk:
    response = client.post('/trips', data=data)
    expected_id = len(TRIPS)
    smtk.assert_called_once()
    assert response.content_type == 'application/json'
    assert response.status_code == 201
    assert load_json_response(response) == {
      'id': expected_id, 
      "from_location": data["from_location"], 
      "to_location": data["to_location"]
    }
    
def test_put_trips(client):
  data = {"from_location": "Some place", "to_location": "Somewhere else"}
  with mock.patch('controllers.trips.send_message_to_kafka', return_value=True) as smtk:
    response = client.put('/trips/1', data=data)
    smtk.assert_called_once()
    assert response.content_type == 'application/json'
    assert response.status_code == 201
    assert load_json_response(response) == {
      'id': 1, 
      "from_location": data["from_location"], 
      "to_location": data["to_location"]
    }

def test_delete_car(client):
  data = TRIPS[0]
  trips_len = len(TRIPS)
  with mock.patch('controllers.trips.send_message_to_kafka', return_value=True) as smtk:
    response = client.delete('/trips/1')
    expected_trips = trips_len - 1
    smtk.assert_called_once()
    assert response.content_type == 'application/json'
    assert response.status_code == 204
    assert expected_trips == len(TRIPS)
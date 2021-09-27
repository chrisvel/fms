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

def test_get_driver(client):
  response = client.get('/drivers/1')
  expected_data = next(item for item in DRIVERS if item["id"] == "1")
  assert response.content_type == 'application/json'
  assert response.status_code == 200
  assert load_json_response(response) == expected_data

def test_get_drivers(client):
  response = client.get('/drivers')
  assert response.content_type == 'application/json'
  assert response.status_code == 200
  assert load_json_response(response) == DRIVERS

def test_post_drivers(client):
  data = {"name": 'John Murdock'}
  with mock.patch('controllers.drivers.send_message_to_kafka', return_value=True) as smtk:
    response = client.post('/drivers', data=data)
    expected_id = len(DRIVERS)
    smtk.assert_called_once()
    assert response.content_type == 'application/json'
    assert response.status_code == 201
    assert load_json_response(response) == {'id': expected_id, 'name': 'John Murdock'}
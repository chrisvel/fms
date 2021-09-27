from kafka import KafkaProducer
import json
import os

def send_message_to_kafka(topic, message):
  producer = KafkaProducer(
    bootstrap_servers=[os.environ.get('BOOTSTRAP_SERVERS')], 
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))
  producer.send(topic, message)
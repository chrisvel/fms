from kafka import KafkaProducer, KafkaConsumer
import json
import os

def consume_messages_from_kafka(topic, data, locks):
  print(f'Starting Kafka listener for topic {topic}')
  try:
    consumer = KafkaConsumer(
      topic, 
      bootstrap_servers=[os.environ.get('BOOTSTRAP_SERVERS')], 
      # group_id=None,
      # auto_offset_reset='earliest',
      # enable_auto_commit=True,
      api_version=(0, 10),
      value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    consumer.poll(timeout_ms=2000)
    for message in consumer:
      print(f'{topic}: {message.value}', flush=True)
      data[topic].append(message.value)
  except:
    print("Error!!")

def send_message_to_kafka(topic, message):
  print(f'Producing message {message} to topic {topic}', flush=True)
  producer = KafkaProducer(
    bootstrap_servers=[os.environ.get('BOOTSTRAP_SERVERS')], 
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))
  producer.send(topic, message)
  producer.flush()
  producer.close()
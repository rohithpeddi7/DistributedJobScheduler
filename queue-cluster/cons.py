# consumer.py
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'jobs-topic',
    bootstrap_servers='localhost:29192',
    auto_offset_reset='earliest',
    group_id='my-group'
)

print("Waiting for messages...")
for message in consumer:
    print(f"Received: {message.value.decode('utf-8')}")

# producer.py
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:29192')

for i in range(10):
    message = f'Hello Kafka {i}'
    producer.send('jobs-topic', message.encode('utf-8'))
    print(f'Sent: {message}')

producer.flush()
producer.close()

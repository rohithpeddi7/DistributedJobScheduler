# producer.py
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:29092')

for i in range(10):
    message = f'Hello Kafka {i}'
    producer.send('my-topic', message.encode('utf-8'))
    print(f'Sent: {message}')

producer.flush()
producer.close()

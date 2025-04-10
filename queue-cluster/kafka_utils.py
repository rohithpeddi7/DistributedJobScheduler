from kafka import KafkaProducer, KafkaConsumer
import json
from config import *

def get_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )

def get_consumer(topic, group_id=None, auto_offset_reset='earliest'):
    return KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=group_id,
        auto_offset_reset=auto_offset_reset,
    )

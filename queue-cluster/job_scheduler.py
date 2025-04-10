import time
import json
from kafka import KafkaProducer
from datetime import datetime, timedelta
import uuid
import random

# Bootstrap server where Kafka is accessible from local machine
KAFKA_BROKER = "localhost:29192"
TOPIC = "jobs-topic"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Simulated Dockerfile references (e.g., Firebase storage URLs or just dummy URLs here)
DOCKERFILE_URLS = [
    "https://firebase.com/job-containers/python-task.dockerfile",
    "https://firebase.com/job-containers/node-task.dockerfile",
    "https://firebase.com/job-containers/java-task.dockerfile",
]

def generate_fake_job():
    return {
        "job_id": str(uuid.uuid4()),
        "scheduled_time": (datetime.utcnow() + timedelta(seconds=5)).isoformat() + "Z",
        "dockerfile_url": random.choice(DOCKERFILE_URLS),
    }

def main():
    print("🗓️  Job scheduler started. Sending job every 15 seconds for demo...")
    while True:
        job = generate_fake_job()
        producer.send(TOPIC, value=job)
        print(f"✅ Published job: {job['job_id']}")
        time.sleep(15)  # Send a job every 15 seconds for demo

if __name__ == "__main__":
    main()

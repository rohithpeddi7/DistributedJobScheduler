import time, threading
from collections import defaultdict
from kafka_utils import get_consumer, get_producer
from config import *
import json

available_workers = set()
worker_last_heartbeat = defaultdict(lambda: time.time())
producer = get_producer()

def listen_availability():
    consumer = get_consumer(WORKER_AVAILABILITY_TOPIC, group_id="my-group")
    for msg in consumer:
        # print("avail ", msg)
        msg = json.loads(msg.value.decode('utf-8'))
        worker_id = msg['worker_id']
        available_workers.add(worker_id)

def listen_heartbeats():
    consumer = get_consumer(WORKER_HEARTBEAT_TOPIC, group_id="my-group")
    for msg in consumer:
        # print("heartbeat", msg)
        msg = json.loads(msg.value.decode('utf-8'))
        worker_id = msg['worker_id']
        worker_last_heartbeat[worker_id] = time.time()

def monitor_workers():
    while True:
        now = time.time()
        to_remove = [w for w, t in worker_last_heartbeat.items() if now - t > 2 * WORKER_HEARTBEAT_INTERVAL]
        for worker in to_remove:
            print(f"[Coordinator] Worker {worker} unresponsive.")
            available_workers.discard(worker)
        time.sleep(2)

def assign_jobs():
    consumer = get_consumer(JOBS_TOPIC, group_id="my-group")
    for msg in consumer:
        if not available_workers:
            print("No workers available, will retry later.")
            time.sleep(2)
            continue
        if msg.value is None or msg.value == {}:
            print("Received None message, skipping.")
            continue
        # print(msg.value)
        job = json.loads(msg.value)
        worker_id = available_workers.pop()
        print(f"[Coordinator] Assigning job {job['job_id']} to {worker_id}")
        producer.send(worker_id, job)

        if not available_workers:
            print("No workers available, will retry later.")
            time.sleep(2)
            continue

if __name__ == "__main__":
    threading.Thread(target=listen_availability, daemon=True).start()
    threading.Thread(target=listen_heartbeats, daemon=True).start()
    threading.Thread(target=monitor_workers, daemon=True).start()
    assign_jobs()

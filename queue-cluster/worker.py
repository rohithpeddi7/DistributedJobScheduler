import time, uuid, threading, requests, subprocess, os
from kafka_utils import get_producer, get_consumer
from config import *
import json

WORKER_ID = f"worker-{uuid.uuid4().hex[:6]}"
producer = get_producer()

def send_heartbeat():
    while True:
        producer.send(WORKER_HEARTBEAT_TOPIC, {"worker_id": WORKER_ID, "timestamp": time.time()})
        time.sleep(WORKER_HEARTBEAT_INTERVAL)

def announce_availability():
    producer.send(WORKER_AVAILABILITY_TOPIC, {"worker_id": WORKER_ID, "timestamp": time.time()})

def fetch_dockerfile(blob_url):
    resp = requests.get(blob_url)
    resp.raise_for_status()
    return resp.text
    # return "some_url"

def build_docker_image(dockerfile_content, image_tag):
    temp_dir = f"./tmp_{WORKER_ID}"
    os.makedirs(temp_dir, exist_ok=True)
    with open(f"{temp_dir}/Dockerfile", "w") as f:
        f.write(dockerfile_content)
    result = subprocess.run(
        ["docker", "build", "-t", image_tag, "."],
        cwd=temp_dir,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return image_tag
    # return "image_tag"

def run_docker_container(image_tag):
    result = subprocess.run(
        ["docker", "run", "--rm", image_tag],
        capture_output=True,
        text=True
    )
    print(result)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout
    # return "output"

def execute_job(job):
    job_id = job['job_id']
    docker_url = job['dockerfile_url']
    image_tag = f"{WORKER_ID}-{job_id}"

    try:
        print(f"{WORKER_ID}: Starting job {job_id}")
        dockerfile = fetch_dockerfile(docker_url)
        build_docker_image(dockerfile, image_tag)
        output = run_docker_container(image_tag)
        print(f"{WORKER_ID}: Job {job_id} finished successfully.")
        status = "success"
    except Exception as e:
        print(f"{WORKER_ID}: Job {job_id} failed: {e}")
        output = str(e)
        status = "failure"

    producer.send(JOB_STATUS_TOPIC, {
        "worker_id": WORKER_ID,
        "job_id": job_id,
        "status": status,
        "output": output,
        "timestamp": time.time(),
        "exit_code": 0 if status == "success" else 1,
    })
    announce_availability()

if __name__ == "__main__":
    announce_availability()
    threading.Thread(target=send_heartbeat, daemon=True).start()
    consumer = get_consumer(WORKER_ID, group_id=WORKER_ID)

    for msg in consumer:
        job = msg.value
        job = json.loads(job.decode('utf-8'))
        execute_job(job)
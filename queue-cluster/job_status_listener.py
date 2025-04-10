# job_status_listener.py

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'job-status',
    bootstrap_servers=['localhost:29192'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='status-monitor-group',
    auto_offset_reset='earliest'
)

print("🔍 Listening to job-status topic...")
for message in consumer:
    status = message.value
    print(f"📦 Job ID: {status['job_id']}")
    print(f"   🧑‍🔧 Worker: {status['worker_id']}")
    print(f"   ✅ Status: {status['status']} (code: {status['exit_code']})")
    print(f"   🕒 Time: {status['timestamp']}")
    print(f"   📄 Logs: {status['logs'][:200]}...\n")

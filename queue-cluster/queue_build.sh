## Run these commands in this order.

sudo docker-compose up --build

docker exec -it kafka1 kafka-topics \
  --create \
  --topic jobs-topic \
  --bootstrap-server localhost:29192 \
  --replication-factor 2 \
  --partitions 3

  # Exec into kafka1 container
docker exec -it kafka1 bash

# 1. Create job-queue topic
kafka-topics --create --topic job-queue \
  --bootstrap-server kafka1:29193 \
  --replication-factor 2 \
  --partitions 3

# 2. Create worker-availability topic
kafka-topics --create --topic worker-availability \
  --bootstrap-server kafka1:29193 \
  --replication-factor 2 \
  --partitions 3

# 3. Create worker-heartbeat topic
kafka-topics --create --topic worker-heartbeat \
  --bootstrap-server kafka1:29193 \
  --replication-factor 2 \
  --partitions 3

# 4. Create job-status topic
kafka-topics --create --topic job-status \
  --bootstrap-server kafka1:29193 \
  --replication-factor 2 \
  --partitions 3

# (Optional) Verify topic list
kafka-topics --list --bootstrap-server kafka1:29193


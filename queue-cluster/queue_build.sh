sudo docker-compose up -d

sudo docker exec -it kafka1 kafka-topics \
  --bootstrap-server localhost:29092 \
  --create \
  --topic jobs \
  --partitions 3 \
  --replication-factor 3
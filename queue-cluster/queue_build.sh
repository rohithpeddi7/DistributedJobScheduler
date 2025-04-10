sudo docker-compose up --build

docker exec -it kafka1 kafka-topics \
  --create \
  --topic jobs-topic \
  --bootstrap-server localhost:29192 \
  --replication-factor 2 \
  --partitions 3

.PHONY: set-up set-up-s3 run stop watch-inventory watch-users watch-orders query

set-up:
	curl -i -X PUT -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/publication-connector/config -d @setup/debezium_config.json
	curl -i -X PUT -H "Accept:application/json" -H "Content-Type:application/json" localhost:8084/connectors/s3-archival-sink/config -d @setup/s3_sink_config.json
	docker exec -i postgres psql -U postgres -d inventory < setup/postgre_data.sql
	docker exec -it postgres psql -U postgres -d inventory -c "ALTER TABLE inventory REPLICA IDENTITY FULL; ALTER TABLE users REPLICA IDENTITY FULL; ALTER TABLE orders REPLICA IDENTITY FULL;"

set-up-s3:
	curl -i -X PUT -H "Accept:application/json" -H "Content-Type:application/json" localhost:8084/connectors/s3-archival-sink/config -d @setup/s3_sink_config.json

# Start processing
run:
	docker exec flink-jobmanager /opt/flink/bin/flink run -py /opt/flink/usrlib/main.py

# Stop all Flink jobs (by restarting the cluster)
stop:
	docker compose restart flink-jobmanager flink-taskmanager

# View Data in Kafka Topics (Live)
watch-inventory:
	docker exec -it schema-registry kafka-avro-console-consumer --bootstrap-server kafka:29092 --topic publication.public.inventory --from-beginning

watch-users:
	docker exec -it schema-registry kafka-avro-console-consumer --bootstrap-server kafka:29092 --topic publication.public.users --from-beginning

watch-orders:
	docker exec -it schema-registry kafka-avro-console-consumer --bootstrap-server kafka:29092 --topic publication.public.orders --from-beginning

# System Logs
logs-kafka:
	docker logs -f kafka

logs-flink-job:
	docker logs -f flink-jobmanager

logs-flink-task:
	docker logs -f flink-taskmanager

logs-source:
	docker logs -f connect-source

logs-sink:
	docker logs -f connect-sink


query:
	docker exec -it flink-jobmanager ./bin/sql-client.sh

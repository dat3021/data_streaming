#  Real-time Data Lakehouse: CDC to S3 with Flink & Paimon

A robust, production-ready data engineering pipeline that captures database changes (CDC), validates them against **Data Contracts**, and sinks them into an **S3-based Data Lakehouse** using Apache Paimon.

##  Architecture
**Postgres** ➔ **Debezium** ➔ **Kafka** ➔ **Apache Flink** ➔ **Apache Paimon (S3)**

1.  **Source**: PostgreSQL database with Full Replica Identity.
2.  **Ingestion**: Debezium (CDC) streaming change events to Kafka via Confluent Avro Schema Registry.
3.  **Processing**: Apache Flink (PyFlink) performing real-time transformations.
4.  **Validation**: Custom Python UDFs enforcing **Data Contracts** (Schema & Business Rules) on every record.
5.  **Sink**: Apache Paimon table format stored on AWS S3, providing ACID transactions and time-travel capabilities.

##  Tech Stack
*   **Engine**: Apache Flink 1.18 (PyFlink)
*   **Table Format**: Apache Paimon (Lakehouse)
*   **CDC**: Debezium + Kafka Connect
*   **Messaging**: Apache Kafka + Schema Registry (Avro)
*   **Storage**: AWS S3
*   **Infrastructure**: Docker & Docker Compose
*   **Orchestration**: Makefile

##  Key Features
*   **End-to-End CDC**: Automatic capture of Inserts, Updates, and Deletes from source tables.
*   **Real-time Data Contracts**: Integrated validation logic using Python UDFs to ensure data quality before it hits the lakehouse.
*   **Schema Evolution**: Automatic handling of schema changes via Paimon's dynamic catalog.
*   **Production Patterns**: Implements best practices like recursive `.gitignore` rules, environment variable management, and automated infrastructure setup.

##  Quick Start
To get this pipeline running on your local machine, follow our [Getting Started Guide](documentation/getting_started.md).

```bash
docker compose up -d
make setup
make run
```

##  Technical Highlights (Resume Points)
*   **ACID Compliance**: Solved data consistency issues in distributed storage by implementing the Paimon table format on S3.
*   **Performance Tuning**: Optimized Flink resource allocation by tuning TaskManager slots and JVM Metaspace for high-throughput connectors.
*   **Module Distribution**: Designed a portable PyFlink execution environment that handles dependency distribution across distributed workers.

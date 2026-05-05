# Getting Started Guide

Follow these steps to set up and run the Data Streaming Pipeline on your local machine.

## Prerequisites
*   Docker & Docker Compose installed.
*   AWS Account with S3 access.
*   Git installed.

---

## 1. Environment Configuration
Since the `.env` file is hidden for security, you must create your own in the root directory.

Create a file named `.env` and add your AWS credentials:
```bash
MY_AWS_ACCESS_KEY_ID=your_access_key
MY_AWS_SECRET_ACCESS_KEY=your_secret_key
MY_AWS_REGION=your_region (e.g., us-east-1)
```

## 2. Launch the Infrastructure
Start all services (Postgres, Kafka, Flink, Schema Registry, etc.):
```bash
docker compose up -d
```
*Wait about 30 seconds for all services to become healthy.*

## 3. Initialize Database & CDC
This command will load the sample data, configure Postgres for CDC, and register the Debezium connector in one go:
```bash
make setup
```

## 4. Run the Flink Pipeline
Submit the PyFlink jobs to start processing data and sinking it to S3:
```bash
make run
```

---

## How to Verify Success
*   **Flink UI**: [http://localhost:8082](http://localhost:8082) - You should see 3 running jobs.
*   **Kafka**: Run `make watch-inventory` to see live events in the topic.
*   **S3**: Check your S3 bucket for the `paimon/` folder containing Parquet data.
*   **SQL**: Run `make query` to enter the Flink SQL Client and query the data lake directly.

FROM flink:1.18-java11

# Switch to root to install packages
USER root

# Install Python, symlink, and uv
RUN apt-get update && apt-get install -y python3-pip python3-dev && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install uv

# Copy pyproject.toml to install dependencies in the image
COPY flink/pyproject.toml /opt/flink/
RUN uv pip install --system -r /opt/flink/pyproject.toml

# Download Flink Connectors (JARs) directly to keep the repo clean
RUN apt-get install -y wget && \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/paimon/paimon-flink-1.18/0.7.0-incubating/paimon-flink-1.18-0.7.0-incubating.jar && \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.1-1.18/flink-sql-connector-kafka-3.0.1-1.18.jar && \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-avro-confluent-registry/1.18.0/flink-sql-avro-confluent-registry-1.18.0.jar && \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/2.8.3-10.0/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar

# Enable S3 support (CRITICAL)
RUN mkdir -p /opt/flink/plugins/s3-hadoop && \
    cp /opt/flink/opt/flink-s3-fs-hadoop-*.jar /opt/flink/plugins/s3-hadoop/

# Ensure permissions for the flink user
RUN chmod -R 755 /opt/flink/lib/ && \
    chmod -R 755 /opt/flink/plugins/ && \
    chmod -R 755 /opt/flink/opt/

# Switch back to flink user
USER flink

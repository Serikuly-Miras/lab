FROM quay.io/strimzi/kafka:1.0.0-kafka-4.2.0

USER root:root

RUN mkdir -p /opt/kafka/plugins/debezium-postgres \
  && curl -fsSL \
    https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/3.4.3.Final/debezium-connector-postgres-3.4.3.Final-plugin.tar.gz \
    | tar -xzf - -C /opt/kafka/plugins/debezium-postgres --strip-components=1

USER 1001
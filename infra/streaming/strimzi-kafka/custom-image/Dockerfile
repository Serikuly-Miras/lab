FROM quay.io/strimzi/kafka:1.0.0-kafka-4.2.0

USER root:root

RUN mkdir -p /opt/kafka/plugins/debezium-postgres \
  && curl -fsSL \
    https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/3.4.3.Final/debezium-connector-postgres-3.4.3.Final-plugin.tar.gz \
    | tar -xzf - -C /opt/kafka/plugins/debezium-postgres --strip-components=1

RUN mkdir -p /opt/kafka/plugins/starrocks-kafka-connector \
  && curl -fsSL \
    https://github.com/StarRocks/starrocks-connector-for-kafka/releases/download/v1.0.6/starrocks-connector-for-kafka-1.0.6-with-dependencies.jar \
    -o /opt/kafka/plugins/starrocks-kafka-connector/starrocks-connector-for-kafka-1.0.6-with-dependencies.jar

USER 1001
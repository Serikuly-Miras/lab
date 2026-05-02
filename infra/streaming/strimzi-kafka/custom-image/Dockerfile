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

# Confluent Avro converter (AvroConverter + schema registry client)
ARG CONFLUENT_VERSION=8.2.0
ARG AVRO_VERSION=1.11.3
RUN mkdir -p /opt/kafka/plugins/confluent-avro-converter \
  && for jar in \
       kafka-connect-avro-converter \
       kafka-connect-avro-data \
       kafka-avro-serializer \
       kafka-schema-registry-client \
       common-utils \
       common-config; do \
     curl -fsSL \
       https://packages.confluent.io/maven/io/confluent/${jar}/${CONFLUENT_VERSION}/${jar}-${CONFLUENT_VERSION}.jar \
       -o /opt/kafka/plugins/confluent-avro-converter/${jar}-${CONFLUENT_VERSION}.jar; \
  done \
  && curl -fsSL \
       https://repo1.maven.org/maven2/org/apache/avro/avro/${AVRO_VERSION}/avro-${AVRO_VERSION}.jar \
       -o /opt/kafka/plugins/confluent-avro-converter/avro-${AVRO_VERSION}.jar

USER 1001
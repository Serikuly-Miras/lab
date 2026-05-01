FROM quay.io/strimzi/kafka:1.0.0-kafka-4.2.0

USER root:root

RUN mkdir -p /opt/kafka/plugins/debezium-postgres \
  && curl -fsSL \
    https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/3.4.3.Final/debezium-connector-postgres-3.4.3.Final-plugin.tar.gz \
    | tar -xzf - -C /opt/kafka/plugins/debezium-postgres --strip-components=1 \
  && curl -fsSL \
    https://repo1.maven.org/maven2/io/debezium/debezium-scripting/3.4.3.Final/debezium-scripting-3.4.3.Final.jar \
    -o /opt/kafka/plugins/debezium-postgres/debezium-scripting-3.4.3.Final.jar \
  && curl -fsSL \
    https://repo1.maven.org/maven2/org/apache/groovy/groovy/4.0.24/groovy-4.0.24.jar \
    -o /opt/kafka/plugins/debezium-postgres/groovy-4.0.24.jar

RUN mkdir -p /opt/kafka/plugins/starrocks-kafka-connector \
  && curl -fsSL \
    https://github.com/StarRocks/starrocks-connector-for-kafka/releases/download/v1.0.6/starrocks-connector-for-kafka-1.0.6-with-dependencies.jar \
    -o /opt/kafka/plugins/starrocks-kafka-connector/starrocks-connector-for-kafka-1.0.6-with-dependencies.jar \
  && curl -fsSL \
    https://repo1.maven.org/maven2/io/debezium/debezium-scripting/3.4.3.Final/debezium-scripting-3.4.3.Final.jar \
    -o /opt/kafka/plugins/starrocks-kafka-connector/debezium-scripting-3.4.3.Final.jar \
  && curl -fsSL \
    https://repo1.maven.org/maven2/org/apache/groovy/groovy/4.0.24/groovy-4.0.24.jar \
    -o /opt/kafka/plugins/starrocks-kafka-connector/groovy-4.0.24.jar

USER 1001
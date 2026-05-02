FROM quay.io/strimzi/kafka:1.0.0-kafka-4.2.0

USER root:root

ARG DEBEZIUM_VERSION=3.4.3.Final
ARG STARROCKS_CONNECTOR_VERSION=1.0.6
ARG CONFLUENT_VERSION=8.2.0

RUN microdnf install -y maven \
  && mkdir -p /tmp/mvn-debezium /tmp/mvn-confluent \
             /opt/kafka/plugins/debezium-postgres \
             /opt/kafka/plugins/confluent-avro-converter \
  \
  && printf '<?xml version="1.0"?>\n\
<project>\n\
  <modelVersion>4.0.0</modelVersion>\n\
  <groupId>tmp</groupId><artifactId>debezium</artifactId><version>1</version>\n\
  <dependencies>\n\
    <dependency>\n\
      <groupId>io.debezium</groupId>\n\
      <artifactId>debezium-connector-postgres</artifactId>\n\
      <version>%s</version>\n\
    </dependency>\n\
  </dependencies>\n\
</project>\n' "${DEBEZIUM_VERSION}" > /tmp/mvn-debezium/pom.xml \
  && mvn -f /tmp/mvn-debezium/pom.xml dependency:copy-dependencies \
       --batch-mode \
       -DoutputDirectory=/opt/kafka/plugins/debezium-postgres \
       -DincludeScope=runtime \
       -Dmdep.useRepositoryLayout=false \
  \
  && printf '<?xml version="1.0"?>\n\
<project>\n\
  <modelVersion>4.0.0</modelVersion>\n\
  <groupId>tmp</groupId><artifactId>confluent</artifactId><version>1</version>\n\
  <repositories>\n\
    <repository><id>confluent</id><url>https://packages.confluent.io/maven</url></repository>\n\
  </repositories>\n\
  <dependencies>\n\
    <dependency>\n\
      <groupId>io.confluent</groupId>\n\
      <artifactId>kafka-connect-avro-converter</artifactId>\n\
      <version>%s</version>\n\
    </dependency>\n\
  </dependencies>\n\
</project>\n' "${CONFLUENT_VERSION}" > /tmp/mvn-confluent/pom.xml \
  && mvn -f /tmp/mvn-confluent/pom.xml dependency:copy-dependencies \
       --batch-mode \
       -DoutputDirectory=/opt/kafka/plugins/confluent-avro-converter \
       -DincludeScope=runtime \
       -Dmdep.useRepositoryLayout=false \
  \
  && rm -rf /tmp/mvn-debezium /tmp/mvn-confluent ~/.m2 \
  && microdnf remove -y maven maven-openjdk17 \
  && microdnf clean all

# StarRocks connector — GitHub releases only, not on Maven Central
RUN mkdir -p /opt/kafka/plugins/starrocks-kafka-connector \
  && curl -fsSL \
    https://github.com/StarRocks/starrocks-connector-for-kafka/releases/download/v${STARROCKS_CONNECTOR_VERSION}/starrocks-connector-for-kafka-${STARROCKS_CONNECTOR_VERSION}-with-dependencies.jar \
    -o /opt/kafka/plugins/starrocks-kafka-connector/starrocks-connector-for-kafka-${STARROCKS_CONNECTOR_VERSION}-with-dependencies.jar

USER 1001
FROM flink:1.20

RUN curl -fsSL \
    https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-postgres-cdc/3.6.0-1.20/flink-sql-connector-postgres-cdc-3.6.0-1.20.jar \
    -o /opt/flink/lib/flink-sql-connector-postgres-cdc-3.6.0-1.20.jar \
  && curl -fsSL \
    https://repo1.maven.org/maven2/com/starrocks/flink-connector-starrocks/1.2.14_flink-1.20/flink-connector-starrocks-1.2.14_flink-1.20.jar \
    -o /opt/flink/lib/flink-connector-starrocks-1.2.14_flink-1.20.jar

RUN mkdir -p /opt/flink/plugins/s3-fs-hadoop \
  && cp /opt/flink/opt/flink-s3-fs-hadoop-*.jar /opt/flink/plugins/s3-fs-hadoop/

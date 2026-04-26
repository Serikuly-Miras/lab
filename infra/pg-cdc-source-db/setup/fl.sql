CREATE TABLE pg_users (
  id INT,
  name STRING,
  email STRING,
  created_at TIMESTAMP_LTZ(6),
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'postgres-cdc',
  'hostname' = 'pg-cdc-source-db-rw.pg-cdc-source-db.svc.cluster.local',
  'port' = '5432',
  'username' = 'pg-cdc',
  'password' = '',
  'database-name' = 'pg-cdc-source-db',
  'schema-name' = 'public',
  'table-name' = 'users',
  'slot.name' = 'flink_users',
  'debezium.plugin.name' = 'pgoutput',
  'debezium.publication.name' = 'dbz_publication'
);

CREATE TABLE pg_shops (
  id INT,
  name STRING,
  city STRING,
  created_at TIMESTAMP_LTZ(6),
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'postgres-cdc',
  'hostname' = 'pg-cdc-source-db-rw.pg-cdc-source-db.svc.cluster.local',
  'port' = '5432',
  'username' = 'pg-cdc',
  'password' = '',
  'database-name' = 'pg-cdc-source-db',
  'schema-name' = 'public',
  'table-name' = 'shops',
  'slot.name' = 'flink_shops',
  'debezium.plugin.name' = 'pgoutput',
  'debezium.publication.name' = 'dbz_publication'
);

CREATE TABLE pg_orders (
  id INT,
  user_id INT,
  shop_id INT,
  amount DECIMAL(10,2),
  status STRING,
  created_at TIMESTAMP_LTZ(6),
  proctime AS PROCTIME(),
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'postgres-cdc',
  'hostname' = 'pg-cdc-source-db-rw.pg-cdc-source-db.svc.cluster.local',
  'port' = '5432',
  'username' = 'pg-cdc',
  'password' = '',
  'database-name' = 'pg-cdc-source-db',
  'schema-name' = 'public',
  'table-name' = 'orders',
  'slot.name' = 'flink_orders',
  'debezium.plugin.name' = 'pgoutput',
  'debezium.publication.name' = 'dbz_publication'
);

CREATE TABLE sr_users (
  id INT,
  name STRING,
  email STRING,
  created_at TIMESTAMP_LTZ(6),
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'starrocks',
  'jdbc-url' = 'jdbc:mysql://starrocks-db-cluster-fe-service.starrocks-db.svc.cluster.local:9030',
  'load-url' = 'starrocks-db-cluster-fe-service.starrocks-db.svc.cluster.local:8030',
  'username' = 'root',
  'password' = '',
  'database-name' = 'cdc',
  'table-name' = 'users',
  'sink.properties.format' = 'json',
  'sink.properties.strip_outer_array' = 'true'
);

CREATE TABLE sr_shops (
  id INT,
  name STRING,
  city STRING,
  created_at TIMESTAMP_LTZ(6),
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'starrocks',
  'jdbc-url' = 'jdbc:mysql://starrocks-db-cluster-fe-service.starrocks-db.svc.cluster.local:9030',
  'load-url' = 'starrocks-db-cluster-fe-service.starrocks-db.svc.cluster.local:8030',
  'username' = 'root',
  'password' = '',
  'database-name' = 'cdc',
  'table-name' = 'shops',
  'sink.properties.format' = 'json',
  'sink.properties.strip_outer_array' = 'true'
);

CREATE TABLE sr_orders (
  id INT,
  user_id INT,
  shop_id INT,
  amount DECIMAL(10,2),
  status STRING,
  created_at TIMESTAMP_LTZ(6),
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'starrocks',
  'jdbc-url' = 'jdbc:mysql://starrocks-db-cluster-fe-service.starrocks-db.svc.cluster.local:9030',
  'load-url' = 'starrocks-db-cluster-fe-service.starrocks-db.svc.cluster.local:8030',
  'username' = 'root',
  'password' = '',
  'database-name' = 'cdc',
  'table-name' = 'orders',
  'sink.properties.format' = 'json',
  'sink.properties.strip_outer_array' = 'true'
);

INSERT INTO sr_users SELECT * FROM pg_users;  
INSERT INTO sr_shops SELECT * FROM pg_shops;
INSERT INTO sr_orders SELECT * FROM pg_orders;

CREATE TABLE sr_orders_flat (
  id INT,
  user_id INT,
  user_name STRING,
  user_email STRING,
  shop_id INT,
  shop_name STRING,
  shop_city STRING,
  amount DECIMAL(10,2),
  status STRING,
  created_at TIMESTAMP_LTZ(6),
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'starrocks',
  'jdbc-url' = 'jdbc:mysql://starrocks-db-cluster-fe-service.starrocks-db.svc.cluster.local:9030',
  'load-url' = 'starrocks-db-cluster-fe-service.starrocks-db.svc.cluster.local:8030',
  'username' = 'root',
  'password' = '',
  'database-name' = 'cdc',
  'table-name' = 'orders_flat',
  'sink.properties.format' = 'json',
  'sink.properties.strip_outer_array' = 'true'
);

INSERT INTO sr_orders_flat
SELECT
  o.id,
  o.user_id,
  u.name AS user_name,
  u.email AS user_email,
  o.shop_id,
  s.name AS shop_name,
  s.city AS shop_city,
  o.amount,
  o.status,
  o.created_at
FROM pg_orders o
JOIN pg_users FOR SYSTEM_TIME AS OF o.proctime u ON o.user_id = u.id
JOIN pg_shops FOR SYSTEM_TIME AS OF o.proctime s ON o.shop_id = s.id;
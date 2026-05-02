CREATE DATABASE cdc;
USE cdc;

CREATE TABLE users (
  id INT NOT NULL,
  name VARCHAR(255),
  email VARCHAR(255),
  created_at DATETIME
) PRIMARY KEY(id)
DISTRIBUTED BY HASH(id)
BUCKETS 1
PROPERTIES ("replication_num" = "1", "fast_schema_evolution" = "true");

CREATE TABLE shops (
  id INT NOT NULL,
  name VARCHAR(255),
  city VARCHAR(255),
  created_at DATETIME
) PRIMARY KEY(id)
DISTRIBUTED BY HASH(id)
BUCKETS 1
PROPERTIES ("replication_num" = "1", "fast_schema_evolution" = "true");

CREATE TABLE orders (
  id INT NOT NULL,
  user_id INT,
  shop_id INT,
  amount DECIMAL(10,2),
  status VARCHAR(50),
  created_at DATETIME
) PRIMARY KEY(id)
DISTRIBUTED BY HASH(id)
BUCKETS 1
PROPERTIES ("replication_num" = "1",    "fast_schema_evolution" = "true");

CREATE TABLE custom_numbers (
  id INT NOT NULL
) PRIMARY KEY(id)
DISTRIBUTED BY HASH(id)
BUCKETS 1
PROPERTIES ("replication_num" = "1", "fast_schema_evolution" = "true");
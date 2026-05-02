CREATE DATABASE DWH;

use DWH;

---

SELECT @@SERVERNAME, @@VERSION;

SELECT * 
FROM sys.dm_server_services 
WHERE servicename LIKE '%Agent%';

---

EXECUTE sys.sp_cdc_enable_db;

CREATE TABLE DWH.dbo.custom_numbers (id int);

EXECUTE sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name = N'custom_numbers',
    @role_name = N'cdc_Admin';

---

SELECT name, is_cdc_enabled 
FROM sys.databases 
WHERE name = DB_NAME();

SELECT * 
FROM cdc.change_tables;

---

INSERT INTO dbo.custom_numbers (id) VALUES (1), (2), (3);

UPDATE dbo.custom_numbers SET id = 99 WHERE id = 1;

DELETE FROM dbo.custom_numbers WHERE id = 2;

---

SELECT 
    __$operation,   -- 1=delete, 2=insert, 3=before update, 4=after update
    __$seqval,
    id
FROM cdc.dbo_custom_numbers_CT
ORDER BY __$seqval;

---

WITH n AS (
    SELECT TOP 10000 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS id
    FROM sys.all_objects a CROSS JOIN sys.all_objects b
)
INSERT INTO dbo.custom_numbers (id)
SELECT id FROM n; 
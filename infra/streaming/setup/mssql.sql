CREATE DATABASE DWH;

use DWH;

---

SELECT @@SERVERNAME, @@VERSION;

SELECT * 
FROM sys.dm_server_services 
WHERE servicename LIKE '%Agent%';

---

EXECUTE sys.sp_cdc_enable_db;

CREATE TABLE DWH.dbo.meteo_data (
    station_id INT,
    latitude FLOAT,
    longitude FLOAT,
    temperature FLOAT,
    recorded_at DATETIME
);

EXECUTE sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name = N'meteo_data',
    @role_name = N'cdc_Admin';

---

SELECT name, is_cdc_enabled 
FROM sys.databases 
WHERE name = DB_NAME();

SELECT * 
FROM cdc.change_tables;

---

WITH n AS (
    SELECT TOP 10000 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS id
    FROM sys.all_objects a CROSS JOIN sys.all_objects b
)
INSERT INTO dbo.meteo_data (station_id, latitude, longitude, temperature, recorded_at)
SELECT
    ABS(CHECKSUM(NEWID())) % 1000,
    RAND(CHECKSUM(NEWID())) * 180 - 90,
    RAND(CHECKSUM(NEWID())) * 360 - 180,
    RAND(CHECKSUM(NEWID())) * 40 - 10,
    DATEADD(SECOND, -id, GETDATE())
FROM n;
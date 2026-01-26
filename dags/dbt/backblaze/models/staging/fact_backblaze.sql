{{ config(
    materialized = 'table',
    post_hook = [ "CREATE INDEX IF NOT EXISTS idx_fact_backblaze_date_serial_number_btree ON {{ this }} USING btree (date, serial_number);" ]
) }}

SELECT
    b.date,
    b.serial_number,
    m.model_id,
    b.capacity_bytes,
    b.failure,
    d.datacenter_id,
    b.cluster_id,
    b.vault_id,
    b.pod_id,
    b.pod_slot_num,
    b.is_legacy_format
FROM
    bronze.backblaze b
    LEFT JOIN {{ ref('dim_backblaze_datacenter') }}
    d
    ON b.datacenter = d.datacenter
    LEFT JOIN {{ ref('dim_backblaze_disk_model') }}
    m
    ON b.model = m.model
WHERE
    b.datacenter IS NOT NULL
    AND b.model IS NOT NULL

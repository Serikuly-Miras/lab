{{ config(
    materialized = 'table',
    pre_hook = "SET enable_seqscan = false;"
) }}

SELECT
    {{ dbt_utils.generate_surrogate_key(['model']) }} AS model_id,
    model,
    CASE
        WHEN model LIKE 'DELL%' THEN 'Dell'
        WHEN model LIKE 'HGST%' THEN 'HGST'
        WHEN model LIKE 'MTFDDA%' THEN 'Micron'
        WHEN model LIKE 'Micron%' THEN 'Micron'
        WHEN model LIKE 'TOSHIBA%' THEN 'Toshiba'
        WHEN model LIKE 'WD%' THEN 'Western Digital'
        WHEN model LIKE 'WUH%' THEN 'Western Digital'
        WHEN model LIKE 'Samsung%' THEN 'Samsung'
        WHEN model LIKE 'Seagate%' THEN 'Seagate'
        WHEN model LIKE 'ST%' THEN 'Seagate'
        WHEN model LIKE 'SSDS%' THEN 'Intel'
        WHEN model LIKE 'CT250%' THEN 'Crucial'
        ELSE 'Other'
    END AS manufacturer,
    CURRENT_TIMESTAMP AS updated_at
FROM
    bronze.backblaze
WHERE
    model IS NOT NULL
GROUP BY
    model

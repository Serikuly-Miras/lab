{{ config(
    materialized = 'table',
    pre_hook = "SET enable_seqscan = false;"
) }}

SELECT
    {{ dbt_utils.generate_surrogate_key(['datacenter']) }} AS datacenter_id,
    datacenter,
    CURRENT_TIMESTAMP AS updated_at
FROM
    bronze.backblaze
WHERE
    datacenter IS NOT NULL
GROUP BY
    datacenter

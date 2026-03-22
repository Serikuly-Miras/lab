WITH per_model_per_day_agg AS (
    SELECT
        bf.date,
        bf.model_id,
        SUM(
            bf.capacity_bytes
        ) AS sum_capacity_bytes
    FROM
        {{ ref('backblaze_fct') }}
        bf
    GROUP BY
        bf.date,
        bf.model_id
)
SELECT
    pmpda.date,
    pmpda.model_id,
    bddm.model,
    bddm.manufacturer,
    pmpda.sum_capacity_bytes
FROM
    per_model_per_day_agg pmpda
    LEFT JOIN {{ ref('backblaze_dim_disk_model') }}
    bddm
    ON pmpda.model_id = bddm.model_id

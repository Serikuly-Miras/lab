WITH total_capacity AS (
    SELECT
        bf.datacenter_id,
        SUM(
            bf.capacity_bytes
        ) AS capacity_bytes
    FROM
        {{ ref('backblaze_fct') }}
        bf
    WHERE
        bf.date = (
            SELECT
                MAX(DATE)
            FROM
                {{ ref('backblaze_fct') }}
        )
    GROUP BY
        bf.datacenter_id
)
SELECT
    tc.datacenter_id,
    bdd.datacenter,
    bdd.city,
    bdd.longitude,
    bdd.latitude,
    tc.capacity_bytes
FROM
    total_capacity tc
    LEFT JOIN {{ ref('backblaze_dim_datacenter') }}
    bdd
    ON bdd.datacenter_id = tc.datacenter_id

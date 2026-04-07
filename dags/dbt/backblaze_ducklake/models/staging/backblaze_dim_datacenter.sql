WITH datacenter AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['b.datacenter']) }} AS datacenter_id,
        b.datacenter
    FROM
        {{ source(
            'datalake',
            'backblaze'
        ) }}
        b
    WHERE
        b.datacenter IS NOT NULL
    GROUP BY
        b.datacenter
)
SELECT
    datacenter.datacenter_id,
    datacenter.datacenter,
    sdc.city,
    sdc.longitude,
    sdc.latitude
FROM
    datacenter
    LEFT JOIN {{ ref('seed_datacenters') }}
    sdc
    ON datacenter.datacenter = sdc.datacenter

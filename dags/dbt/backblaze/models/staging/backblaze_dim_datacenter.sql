SELECT
    {{ dbt_utils.generate_surrogate_key(['datacenter']) }} AS datacenter_id,
    datacenter
FROM
    {{ source(
        'bronze',
        'backblaze'
    ) }}
    b
WHERE
    datacenter IS NOT NULL
GROUP BY
    datacenter

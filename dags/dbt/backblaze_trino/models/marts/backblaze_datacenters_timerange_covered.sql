SELECT
    MIN(
        bf.date
    ) AS first_date,
    MAX(
        bf.date
    ) AS last_date
FROM
    {{ ref('backblaze_fct') }}
    bf

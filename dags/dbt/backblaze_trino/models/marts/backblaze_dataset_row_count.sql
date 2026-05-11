SELECT
    COUNT(*) AS total_rows
FROM
    {{ ref('backblaze_fct') }}
    bf

WITH measurements AS (
    SELECT
        DATE_TRUNC(
            'month',
            bf.date
        ) AS MONTH,
        SUM(CAST(bf.capacity_bytes AS largeint)) AS total_capacity_bytes,
        COUNT(
            DISTINCT bf.serial_number
        ) AS drives_count
    FROM
        {{ ref('backblaze_fct') }}
        bf
    WHERE
        DATE_TRUNC(
            'month',
            bf.date
        ) IN (
            SELECT
                DATE_TRUNC('month', MAX(DATE))
            FROM
                {{ ref('backblaze_fct') }}
            UNION ALL
            SELECT
                DATE_TRUNC('month', MAX(DATE)) - INTERVAL 1 MONTH
            FROM
                {{ ref('backblaze_fct') }}
        )
    GROUP BY
        DATE_TRUNC(
            'month',
            bf.date
        )
)
SELECT
    m1.month AS current_month,
    m1.total_capacity_bytes AS current_month_capacity_bytes,
    m1.drives_count AS current_month_drives_count,
    m2.month AS previous_month,
    m2.total_capacity_bytes AS previous_month_capacity_bytes,
    m2.drives_count AS previous_month_drives_count,
    (
        m1.total_capacity_bytes - m2.total_capacity_bytes
    ) AS capacity_change_bytes,
    (
        m1.drives_count - m2.drives_count
    ) AS drives_change_count,
    CASE
        WHEN m2.total_capacity_bytes = 0 THEN NULL
        ELSE (
            (
                m1.total_capacity_bytes - m2.total_capacity_bytes
            ) / m2.total_capacity_bytes
        ) * 100
    END AS capacity_change_percentage
FROM
    measurements m1
    JOIN measurements m2
    ON m1.month = m2.month + INTERVAL 1 MONTH

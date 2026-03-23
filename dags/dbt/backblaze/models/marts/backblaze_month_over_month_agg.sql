WITH measurements AS (
    SELECT
        bf.date,
        SUM(
            bf.capacity_bytes
        ) AS total_capacity_bytes,
        COUNT(
            DISTINCT bf.serial_number
        ) AS drives_count
    FROM
        {{ ref('backblaze_fct') }}
        bf
    WHERE
        bf.date IN (
            SELECT
                MAX(DATE) AS d
            FROM
                {{ ref('backblaze_fct') }}
            UNION ALL
            SELECT
                MAX(DATE) - INTERVAL '1 MONTH' AS d
            FROM
                {{ ref('backblaze_fct') }}
        )
    GROUP BY
        bf.date
)
SELECT
    m1.date AS current_month_date,
    m1.total_capacity_bytes AS current_month_capacity_bytes,
    m1.drives_count AS current_month_drives_count,
    m2.date AS previous_month_date,
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
    ON m1.date = m2.date + INTERVAL '1 MONTH'

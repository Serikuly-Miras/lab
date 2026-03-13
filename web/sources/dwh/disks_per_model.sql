SELECT
    model,
    COUNT(1)
FROM
    bronze.backblaze
WHERE
    DATE = '2025-09-30'
GROUP BY
    model;

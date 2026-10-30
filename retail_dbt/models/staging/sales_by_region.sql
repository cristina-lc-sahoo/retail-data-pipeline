SELECT
    region,
    COUNT(*) AS order_count,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total), 2) AS total_sales
FROM {{ ref('stg_sales') }}
GROUP BY region

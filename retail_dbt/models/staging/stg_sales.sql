SELECT
    order_id,
    CAST(date AS DATE) AS sale_date,
    TRIM(product) AS product,
    quantity,
    unit_price,
    total,
    TRIM(region) AS region,
    TRIM(salesperson) AS salesperson
FROM raw.sales

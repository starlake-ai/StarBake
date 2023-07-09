SELECT
    p.product_id,
    SUM(op.quantity) AS total_units_sold,
    SUM(op.quantity * op.price) AS total_revenue,
    SUM(op.quantity * op.price) / SUM(op.quantity) AS average_revenue_per_unit
FROM
    Products p
        JOIN (
        SELECT
            order_id,
            product_id,
            quantity,
            price
        FROM
            Orders,
            UNNEST(products) AS product
    ) op ON p.product_id = op.product_id
GROUP BY
    p.product_id;

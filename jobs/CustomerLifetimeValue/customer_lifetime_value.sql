SELECT
    c.customer_id,
    SUM(o.total_spend) AS total_spend_to_date,
    AVG(o.total_spend) AS average_spend_per_order,
    COUNT(o.order_id) AS frequency_of_orders
FROM
    Customers c
        JOIN (
        SELECT
            customer_id,
            order_id,
            SUM(price * quantity) AS total_spend
        FROM
            Orders,
            UNNEST(products) AS product
        GROUP BY
            customer_id,
            order_id
    ) o ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id;

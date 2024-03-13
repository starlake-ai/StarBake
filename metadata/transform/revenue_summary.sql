SELECT
    o.order_id,
    o.timestamp AS order_date,
    SUM(ol.quantity * ol.sale_price) AS total_revenue
FROM
    "order" o
    JOIN order_line ol ON o.order_id = ol.order_id
GROUP BY
    o.order_id, o.timestamp;

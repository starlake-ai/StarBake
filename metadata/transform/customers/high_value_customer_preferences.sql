SELECT
    hvc.customer_id,
    cp.product_id,
    cp.affinity_score
FROM
    high_value_customers hvc
        JOIN CustomerProductAffinity cp ON hvc.customer_id = cp.customer_id;

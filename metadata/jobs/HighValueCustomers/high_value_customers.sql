SELECT
    customer_id,
    total_spend_to_date,
    RANK() OVER (ORDER BY total_spend_to_date DESC) AS rank
FROM
    CustomerLifetimeValue;

SELECT
    p.product_id,
    SUM(i.price * pi.quantity) AS cost_of_production,
    SUM(op.quantity * op.price) AS total_revenue,
    (SUM(op.quantity * op.price) - SUM(i.price * pi.quantity)) / SUM(op.quantity * op.price) AS profit_margin_per_product
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
        JOIN (
        SELECT
            product_id,
            ingredient_id,
            quantity
        FROM
            ProductIngredients
    ) pi ON p.product_id = pi.product_id
        JOIN Ingredients i ON pi.ingredient_id = i.ingredient_id
GROUP BY
    p.product_id;

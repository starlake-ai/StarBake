SELECT
    p.product_id,
    pp.total_units_sold,
    pp.total_revenue,
    pp.profit_margin_per_product
FROM
    TopSellingProducts tp
        JOIN ProductProfitability pp ON tp.product_id = pp.product_id;

import pathlib

import pandas as pd
import numpy as np
import json
import glob
pd.set_option('display.max_colwidth', None)

source_dir = str(pathlib.Path(__file__).parent.resolve().parent) + '/_data/source'
expected_dir = str(pathlib.Path(__file__).parent.resolve().parent) + '/_data/expected'

# Customers
customer_cols = ["customer_id", "customer_full_name", "customer_join_date", "total_spend_to_date", "average_spend_per_order", "frequency_of_orders"]

# ProductPerformance
product_performance_cols = ["product_id", "product_name", "total_units_sold", "total_revenue", "average_revenue_per_unit"]

# ProductProfitability
product_profitability_cols = ["product_id", "product_name", "profit_margin_per_product"]

# HighValueCustomers
high_value_customers_cols = ["customer_id", "customer_full_name", "lifetime_value"]

# TopSellingProducts
top_selling_products_cols = ["product_id", "product_name", "units_sold", "revenue"]

# MostProfitableProducts
most_profitable_products_cols = ["product_id", "product_name", "profit_margin"]

# TopSellingProfitableProducts
top_selling_profitable_products_cols = ["product_id", "product_name", "units_sold", "revenue", "profit_margin"]

# HighValueCustomerPreferences
high_value_customer_preferences_cols = ["customer_id", "customer_full_name", "product_id", "product_name", "affinity_score"]

# Function to generate customer lifetime value data

def handle_customer_data(df_customers):
    df_customers['customer_full_name'] = df_customers['first_name'] + ' ' + df_customers['last_name']
    df_customers['customer_join_date'] = df_customers['join_date']

def generate_customer_lifetime_value_data(df_customers, df_orders):
    df_orders["total_order_value"] = df_orders["products"].apply(lambda x: sum([prod["price"] * prod["quantity"] for prod in x]))
    df_orders_grouped = df_orders.groupby("customer_id").agg(
        total_spend_to_date=("total_order_value", "sum"),
        average_spend_per_order=("total_order_value", "mean"),
        frequency_of_orders=("order_id", "count")
    ).reset_index()

    df_customer_lifetime_value = pd.merge(df_customers, df_orders_grouped, on="customer_id")
    df_customer_lifetime_value = df_customer_lifetime_value[customer_cols]
    return df_customer_lifetime_value

# Function to generate product performance data
def generate_product_performance_data(df_products, df_orders):
    df_orders_exploded = df_orders.explode("products")
    df_orders_exploded["units_sold"] = df_orders_exploded["products"].apply(lambda x: x["quantity"])
    df_orders_exploded["revenue"] = df_orders_exploded["products"].apply(lambda x: x["quantity"] * x["price"])


    # Create a new DataFrame from the 'products' series of dictionaries
    products_df = df_orders_exploded['products'].apply(pd.Series)
    # Concatenate the new 'products' DataFrame with the original DataFrame
    df_orders_exploded = pd.concat([df_orders_exploded.drop('products', axis=1), products_df], axis=1)

    df_product_performance = df_orders_exploded.groupby("product_id").agg(
        total_units_sold=("units_sold", "sum"),
        total_revenue=("revenue", "sum"),
        average_revenue_per_unit=("revenue", "mean")
    ).reset_index()

    df_product_performance = pd.merge(df_product_performance, df_products[["product_id", "name"]], on="product_id")
    df_product_performance['product_name'] = df_product_performance['name']
    df_product_performance = df_product_performance[product_performance_cols]
    return df_product_performance

# Function to generate product profitability data
def generate_product_profitability_data(df_products, df_ingredients):# Explode the 'ingredients' column

    df_ingredients['ingredient_price'] = df_ingredients['price']
    df_ingredients['ingredient_name'] = df_ingredients['name']
    df_ingredients = df_ingredients[['ingredient_id', 'ingredient_name', 'ingredient_price', 'quantity_in_stock']]

    df_products_exploded = df_products.explode('ingredients')

    # Create a new DataFrame from the 'ingredients' series of dictionaries
    ingredients_df = df_products_exploded['ingredients'].apply(pd.Series)

    # Concatenate the new 'ingredients' DataFrame with the original DataFrame
    df_products_exploded = pd.concat([df_products_exploded.drop('ingredients', axis=1), ingredients_df], axis=1)

    # Now you can merge with 'ingredient_id'
    df_product_profitability = pd.merge(df_products_exploded, df_ingredients, left_on="ingredient_id", right_on="ingredient_id")
    df_product_profitability["total_ingredient_cost"] = df_product_profitability["quantity"] * df_product_profitability["ingredient_price"]
    # Create a new DataFrame from the 'details' series of dictionaries
    details_df = df_product_profitability['details'].apply(pd.Series)

    # Concatenate the new 'details' DataFrame with the original DataFrame
    df_product_profitability = pd.concat([df_product_profitability.drop('details', axis=1), details_df], axis=1)

    # Now you can calculate the profit margin per product
    df_product_profitability["profit_margin_per_product"] = df_product_profitability["price"] - df_product_profitability["total_ingredient_cost"]
    df_product_profitability['product_name'] = df_product_profitability['name']
    df_product_profitability = df_product_profitability[product_profitability_cols]
    return df_product_profitability

# Function to generate high-value customers data
def generate_high_value_customers_data(df_customer_lifetime_value):
    df_high_value_customers = df_customer_lifetime_value.sort_values("total_spend_to_date", ascending=False)
    df_high_value_customers = df_high_value_customers.head(3)
    df_high_value_customers = df_high_value_customers[high_value_customers_cols]
    return df_high_value_customers

# Function to generate top-selling products data
def generate_top_selling_products_data(df_product_performance):
    df_top_selling_products = df_product_performance.sort_values("total_units_sold", ascending=False)
    df_top_selling_products = df_top_selling_products.head(3)
    df_top_selling_products = df_top_selling_products[top_selling_products_cols]
    return df_top_selling_products

# Function to generate most profitable products data
def generate_most_profitable_products_data(df_product_profitability):
    df_most_profitable_products = df_product_profitability.sort_values("profit_margin_per_product", ascending=False)
    df_most_profitable_products = df_most_profitable_products.head(3)
    df_most_profitable_products["profit_margin"] = df_most_profitable_products["profit_margin_per_product"]
    print(df_most_profitable_products)
    df_most_profitable_products = df_most_profitable_products[most_profitable_products_cols]
    return df_most_profitable_products

# Function to generate top-selling profitable products data
def generate_top_selling_profitable_products_data(df_top_selling_products, df_most_profitable_products):
    df_top_selling_profitable_products = pd.merge(df_top_selling_products, df_most_profitable_products, on="product_id")
    df_top_selling_profitable_products = df_top_selling_profitable_products[top_selling_profitable_products_cols]
    return df_top_selling_profitable_products

# Function to generate high-value customer preferences data
def generate_high_value_customer_preferences_data(df_high_value_customers, df_orders):
    df_high_value_customer_preferences = df_orders.explode("products")
    df_high_value_customer_preferences = pd.merge(df_high_value_customer_preferences, df_high_value_customers, on="customer_id")
    df_high_value_customer_preferences = df_high_value_customer_preferences[high_value_customer_preferences_cols]
    return df_high_value_customer_preferences

# Loop over each day's data
for i in range(1, 6):
    df_customers = pd.read_csv(f"{source_dir}/day_{i}/customers_{i}.csv")
    handle_customer_data(df_customers)
    df_ingredients = pd.read_csv(f"{source_dir}/day_{i}/ingredients_{i}.tsv", sep='\t')
    df_products = pd.read_json(f"{source_dir}/day_{i}/products_{i}.json", lines=True)
    df_orders = pd.read_json(f"{source_dir}/day_{i}/orders_{i}.json")

    # Create expected directory
    expected_dir_path = f"{expected_dir}/day_{i}"
    pathlib.Path(expected_dir_path).mkdir(parents=True, exist_ok=True)

    # Generate expected data
    df_customer_lifetime_value = generate_customer_lifetime_value_data(df_customers, df_orders)
    df_product_performance = generate_product_performance_data(df_products, df_orders)
    df_product_profitability = generate_product_profitability_data(df_products, df_ingredients)
    # df_high_value_customers = generate_high_value_customers_data(df_customer_lifetime_value)
    # df_top_selling_products = generate_top_selling_products_data(df_product_performance)
    df_most_profitable_products = generate_most_profitable_products_data(df_product_profitability)
    # df_top_selling_profitable_products = generate_top_selling_profitable_products_data(df_top_selling_products, df_most_profitable_products)
    # df_high_value_customer_preferences = generate_high_value_customer_preferences_data(df_high_value_customers, df_orders)

    # Save to CSV files
    df_customer_lifetime_value.to_csv(f"{expected_dir_path}/customer_lifetime_value.csv", index=False)
    df_product_performance.to_csv(f"{expected_dir_path}/product_performance.csv", index=False)
    df_product_profitability.to_csv(f"{expected_dir_path}/product_profitability.csv", index=False)
    # df_high_value_customers.to_csv(f"{expected_dir_path}/high_value_customers.csv", index=False)
    # df_top_selling_products.to_csv(f"{expected_dir_path}/top_selling_products.csv", index=False)
    # df_most_profitable_products.to_csv(f"{expected_dir_path}/most_profitable_products.csv", index=False)
    # df_top_selling_profitable_products.to_csv(f"{expected_dir_path}/top_selling_profitable_products.csv", index=False)
    # df_high_value_customer_preferences.to_csv(f"{expected_dir_path}/high_value_customer_preferences.csv", index=False)
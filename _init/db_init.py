import os
import sys
import time

from faker import Faker
import random
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

fake = Faker()

# Sample bakery category and products
bakery_categories_products = {
    'Cakes': ['Chocolate Cake', 'Vanilla Cake', 'Carrot Cake'],
    'Cookies': ['Chocolate Chip Cookies', 'Gingerbread Cookies', 'Sugar Cookies'],
    'Breads': ['Baguette', 'Whole Wheat Bread', 'Croissant'],
    'Pies': ['Apple Pie', 'Blueberry Pie', 'Pecan Pie']
}

# Number of records to generate
num_customers = 30
num_orders = 100

# Check command-line arguments
if len(sys.argv) != 2 or sys.argv[1].lower() not in ['postgres', 'mysql', 'mssql']:
    print("Usage: python filename.py [postgres|mysql|mssql]")
    sys.exit()

#GET var env
DB_HOSTNAME = os.environ.get('DB_HOSTNAME', "localhost")

def create_db_engine(database_system):
    if database_system == 'postgres':
        return create_engine(f'postgresql://postgres:password@{DB_HOSTNAME}:5432/starbake')
    elif database_system == 'mysql':
        return create_engine(f'mysql://root:password@{DB_HOSTNAME}:3306/starbake')
    elif database_system == 'mssql':
        return create_engine(
            f'mssql+pyodbc://sa:01pass_WORD@{DB_HOSTNAME}:1433/master?driver=ODBC+Driver+17+for+SQL+Server')


engine = create_db_engine(sys.argv[1].lower())
# Connection retry logic
retry_limit = 5
retry_count = 0
while retry_count < retry_limit:
    try:
        print(f"Connecting to the database.{engine.url}")
        connection = engine.connect()
        break
    except OperationalError as oe:
        retry_count += 1
        print(f"Connection failed. Attempt {retry_count}/{retry_limit}. Will retry after 5 seconds.")
        print(f"Error: {oe}")
        time.sleep(2)
else:
    raise OperationalError("Failed to connect after 5 attempts. Please check your database settings.")

# Generate data for customers
customers_data = {(i + 1, fake.first_name(), fake.last_name(), fake.email(), fake.date_time_this_year()) for i in
                  range(num_customers)}
df_customers = pd.DataFrame(customers_data, columns=['customer_id', 'first_name', 'last_name', 'email', 'join_date'])
df_customers.to_sql('customers', engine, if_exists='append', index=False)

# Generate data for products
product_id = 0
products_data = []

for category, products in bakery_categories_products.items():
    for product_name in products:
        product_id += 1
        price = round(random.uniform(5, 30), 2)
        description = 'Description for ' + product_name
        products_data.append((product_id, product_name, price, description, category))

df_products = pd.DataFrame(products_data, columns=['product_id', 'name', 'price', 'description', 'category'])
df_products.to_sql('products', engine, if_exists='append', index=False)

# Generate data for orders and order_lines
statuses = ["Delivered", "Pending", "Cancelled"]

orders_data = []
order_lines_data = []

for i in range(num_orders):
    customer_id = random.choice(range(1, num_customers + 1))  # Random customer id
    order_datetime = fake.date_time_this_year()
    status = random.choice(statuses)
    orders_data.append((i + 1, customer_id, order_datetime, status))

    product_info = random.choice(products_data)
    product_id = product_info[0]
    quantity = random.randint(1, 5)
    price = product_info[2]  # Use product price from product data
    order_lines_data.append((i + 1, product_id, quantity, price))

df_orders = pd.DataFrame(orders_data, columns=['order_id', 'customer_id', 'timestamp', 'status'])
df_orders.to_sql('orders', engine, if_exists='append', index=False)

df_order_lines = pd.DataFrame(order_lines_data, columns=['order_id', 'product_id', 'quantity', 'price'])
df_order_lines.to_sql('order_lines', engine, if_exists='append', index=False)

print("Data generated and inserted into the database successfully!")

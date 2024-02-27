## StarBake

Welcome to the StarBake project tutorial! This guide will walk you through the end-to-end process of using Starlake to transform raw operational data into insightful business analytics.

StarBake aims to offer hands-on experience with Starlake, using Google BigQuery as the primary data warehousing solution. This tutorial covers essential aspects of the data transformation process, including 
- extracting data from various sources,
- raw data ingestion
- transformation into business insights
- orchestrating the ingestion and transformation process.



### 1. Data Structure To Extract

StarBake project focuses mainly on four tables: Customers, Orders, OrderLines, and Products. Each table contains daily updated operational data from the e-commerce bakery business. The databases use specific identifiers (customer_id, order_id, product_id) to form relationships.

1. **customers:** This table contains information about the bakery's customers. The data for this table arrives in CSV format, updated daily with deltas.
    - `customer_id`: A unique identifier for each customer.
    - `first_name`: The customer's first name.
    - `last_name`: The customer's last name.
    - `email`: The customer's email address.
    - `join_date`: The date when the customer joined.

2. **orders:** This table contains information about the bakery's orders. The data for this table arrives in JSON format, updated daily with deltas.
    - `order_id`: A unique identifier for each order.
    - `customer_id`: An identifier for the customer who placed the order, referencing `Customers.customer_id`.
    - `timestamp`: The date and time when the order was placed.
    - `status`: The status of the order, like 'placed', 'shipped', or 'delivered'.

3. **order_lines:** This table contains information about the individual items within each order. The data for this table arrives in CSV format, updated daily with deltas.
    - `order_id`: An identifier for the order, referencing `Orders.order_id`.
    - `product_id`: An identifier for the product, referencing `Products.product_id`.
    - `quantity`: The quantity of this product in the order.
    - `price`: The price of the product at the time of ordering.

4. **products:** This table contains information about the bakery's products. The data for this table arrives in JSON_ND format, updated daily with deltas.
    - `product_id`: A unique identifier for each product.
    - `name`: The product's name.
    - `price`: The current price of the product.
    - `description`: A detailed description of the product.
    - `category`: The category of the product, like 'bread', 'cake', or 'pastry'.

```mermaid
erDiagram
    ORDERS ||--o{ CUSTOMERS : "is placed by"
    PRODUCTS ||--o{ ORDER_LINES : "in"
    ORDERS ||--o{ ORDER_LINES : "includes"

    CUSTOMERS {
        string customer_id PK
        string first_name
        string last_name
        string email
        date join_date
    }

    ORDERS {
        string order_id PK
        string customer_id FK
        datetime timestamp
        string status
    }

    ORDER_LINES {
        string order_id FK
        string product_id FK
        int quantity
        decimal price
    }

    PRODUCTS {
        string product_id PK
        string name
        decimal price
        string description
        string category
    }

```


### 2. Data Ingestion


### 3. Business Insights Transformations:

1. **CustomerOrders:** A table derived from the `Customers` and `Orders` tables, displaying the customer ID, customer's full name, total number of orders made by each customer, and the average order value.

2. **OrderDetails:** A table formed from the `Orders`, `OrderLines`, and `Products` tables. The OrderDetails table includes all the essential details of an order made from a particular customer, including order ID, customer ID, the timestamp of the order, order status, and an array of order line items.

3. **CustomerOrderDetails:** An extension of the `OrderDetails` and `CustomerOrders` tables, this new table provides a comprehensive view into the behavior of each customer, containing information about order details along with the customer's full name, total number of orders, and the average order value.

```mermaid
classDiagram

    Products --|> OrderDetails: uses
    Orders --|> OrderDetails: uses
    Customers --|> CustomerOrders: uses
    Orders --|> CustomerOrders: uses
    OrderLines --|> OrderDetails: uses

    OrderDetails --|> CustomerOrderDetails: uses
    CustomerOrders --|> CustomerOrderDetails: uses

    class Customers{
    }

    class Orders {
    }

    class OrderLines {
    }

    class Products {
    }

    class OrderDetails {
        string order_id PK
        string customer_id FK
        datetime timestamp
        string status
        OrderLines order_lines[] array
    }

    class CustomerOrders {
        string customer_id FK
        string customer_full_name
        integer total_orders
        decimal average_order_value
    }

    class CustomerOrderDetails {
        string customer_id FK
        string customer_full_name
        integer total_orders
        decimal average_order_value
        OrderLines order_lines[] array
    }


```

### 4. Orchestration


## How to run
Please check [HOW_TO_RUN.md](HOW_TO_RUN.md)

#### Workflow
- [ ] Add .vscode project configuration that include the necessary plugins.
- [ ] Add sqlfluff as sql formatter
- [ ] Add pre-hook to compile & format the code before commit

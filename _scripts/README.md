# StarBake Data Generation Script

## Overview

This script generates synthetic test data for the StarBake project, a demonstrative project designed to showcase the usage of Starlake for data transformation and analytics in an e-commerce bakery business setting. The script generates data for six primary tables: Customers, Orders, Products, Ingredients, and ProductIngredients.

## Data Generation

For each table, the script generates 5 data files. Each file contains a set of unique records, where the primary key ID is an incremental integer starting from 1. The data fields are designed to be relevant to a bakery business. For example, the product names are common bakery items, and the ingredient names are common baking ingredients.

The generated data is saved in various formats (CSV, TSV, JSON), as per the requirements of the StarBake project. The files are then zipped into a single .zip file for easy distribution and storage.

## How to Run

This script is designed to be run in a Python environment. You need to install the libraries needed using pip:

```
pip install -r requirements.txt
```

To run the script, simply execute the script file with a Python interpreter:

```
python starbake_data_generation.py
```

The script does not take any arguments. Once the script is run, it will automatically generate the data, save the data files in the data folder & in the correct formats.

Please note that due to the use of random data generation, the output will be different each time the script is run.

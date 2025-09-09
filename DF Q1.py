# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 10:04:14 2025

@author: Shuaib Boolay
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# df = pd.read_csv("C:/Users/SD 2/Documents/Data Science Project/Generated file CSV.csv")

n = 200 # number of rows

# Creates n unique transaction IDs
# Uses a list comprehension and .zfill(4) to pad numbers with zeros for a consistent format.
transaction_ids = [f"T{str(i).zfill(4)}" for i in range(1, n+1)] 

# Builds 150 unique customer IDs
customer_ids = [f"C{str(i).zfill(3)}" for i in range(1, 151)]
# randomly selects a customer for each transaction (customers can repeat)
customer_column = np.random.choice(customer_ids, n)

# Defines age group buckets and randomly assigns one to each transaction.
customer_age_range = ["18-25", "26-35", "36-45", "46-60", "60+"]
customer_age_column = np.random.choice(customer_age_range, n)

# product_mapping is a dictionary mapping each category to a list of possible product names.
# categories is a random category for each transaction.
# products picks a random product from the chosen category for each transaction this ensures product names always match their category.
product_mapping = {
    "Appliances": ["Oven", "Washing Machine", "Microwave", "Fridge"],
    "Dining": ["Bar Stool", "Dining Chair", "Dining Table"],
    "Bedroom": ["Bedside Table", "Bed Frame", "Wardrobe", "Mattress"],
    "Electronics": ["Smartphone", "Laptop", "Speaker", "TV"],
    "Decor": ["Paintings", "Lamp", "Curtains", "Rug"],
    "Living Room": ["Sofa", "Coffee Table", "TV Stand", "Bookshelf"]
    }
categories = np.random.choice(list(product_mapping.keys()), n)
products = [np.random.choice(product_mapping[cat])for cat in categories]

# This dictionary assigns a fixed Unit Price (R) to every product name.
unit_price_mapping = {
    "Smartphone": 5000,
    "Oven": 20000,
    "Washing Machine": 12000,
    "Sofa": 7000,
    "Dining Table": 4500,
    "Dining Chair": 1000,
    "Bed Frame": 3000,
    "TV": 2000,
    "TV Stand": 500,
    "Coffee Table": 1000,
    "Lamp": 550,
    "Paintings": 350,
    "Wardrobe": 800,
    "Microwave": 4000,
    "Fridge": 5000,
    "Bar Stool": 500,
    "Bedside Table": 800,
    "Mattress": 3000,
    "Laptop": 5000,
    "Speaker": 200,
    "Curtains": 400,
    "Bookshelf": 1200,
    "Rug": 800,
    }

# Random integer quantity between 1 and 7 (upper bound 8 is exclusive) for each transaction.
quantity = np.random.randint(1,8,n)

# Creates a date range and picks a random offset of days for each transaction
# random_dates becomes an array of random dates between start_date and end_date - 1 day
# pd.to_datetime() converts string into datetime objects
# Subtracting the two dates gives a Timedelta - represents the difference between two dates
# .days extracts the number of days in that period.
# np.random.randint() generates n integers between 0 and n_days 
# Each integer represents how many days after the start date a transaction happened
start_date = pd.to_datetime("2024-01-01")
end_date = pd.to_datetime("2025-09-01")
n_days = (end_date - start_date).days
random_days = np.random.randint(0, n_days, n)
random_dates = start_date + pd.to_timedelta(random_days, unit="d")

# Randomly assigns a payment method for each transaction.
payment_method = ["Credit Card", "Debit Card", "Cash"]
payment_method_column = np.random.choice(payment_method, n)

df = pd.DataFrame({
    "Transaction ID": transaction_ids,
    "Customer ID": customer_column,
    "Customer Age Group": customer_age_column,
    "Product Category": categories,
    "Product Name": products,
    #"Unit Price (R)"]): ["Product Name"].map(unit_price_mapping),
    "Quantity Purchased": quantity,
    #"Total Sale Amount": ,
    "Date of Purchase": random_dates,
    "Payment Method": payment_method_column
    })

# .map(unit_price_mapping) looks up the price for each Product Name and creates the Unit Price (R) column.
# df.pop("Unit Price (R)") removes that column from the DataFrame while returning the column data.
# df.insert(5, "Unit Price (R)", unit_price_col) inserts the unit price column into the 6th column. This reorders columns so unit price sits after product name.
df["Unit Price (R)"] = df["Product Name"].map(unit_price_mapping)
unit_price_col = df.pop("Unit Price (R)")
df.insert(5, "Unit Price (R)", unit_price_col)

# Multiplies Quantity Purchased × Unit Price (R) to create Total Sale Amount.
# df.pop removes "Total Sale Amount" from the df, df.insert, inserts it at the 8th column
df["Total Sale Amount"] = df["Quantity Purchased"] * df["Unit Price (R)"]
tot_sale_col = df.pop("Total Sale Amount")
df.insert(7, "Total Sale Amount", tot_sale_col)
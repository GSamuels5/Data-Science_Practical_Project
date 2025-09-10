# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 10:04:14 2025

@author: Shuaib Boolay
"""
'''
Question 1 - Data Creation 
'''
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# df = pd.read_csv("C:/Users/SD 2/Documents/Data Science Project/Generated file CSV.csv")
# df = pd.read_csv("SLG Final Sales Save.csv")

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
    "Smartphone": 5300,
    "Oven": 13100,
    "Washing Machine": 10500,
    "Sofa": 6800,
    "Dining Table": 3500,
    "Dining Chair": 799,
    "Bed Frame": 3000,
    "TV": 6000,
    "TV Stand": 1100,
    "Coffee Table": 1400,
    "Lamp": 550,
    "Paintings": 350,
    "Wardrobe": 2900,
    "Microwave": 1100,
    "Fridge": 7900,
    "Bar Stool": 650,
    "Bedside Table": 800,
    "Mattress": 1600,
    "Laptop": 5000,
    "Speaker": 200,
    "Curtains": 400,
    "Bookshelf": 700,
    "Rug": 1299,
    }

# Random integer quantity between 1 and 5 (upper bound 6 is exclusive) for each transaction.
quantity = np.random.randint(1,6,n)

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

df = pd.read_csv("SLG Final Sales Save.csv")
df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"], errors="coerce")

'''
Question 2 – Data Cleaning & Visualization (40 marks)
Clean your dataset: remove missing/zero values and duplicates.

'''
#Checking for duplicate values and removing it
print(df.describe)
print(df.info())

df = df.drop_duplicates()
print(df.info())

#Now I will be removing missing values
df = df.dropna()
print(df.info())

#Then I will be creating a frequency table for the Product Category
product_cat = df['Product Category'].value_counts()
print('This is the frequency table for Product Category column: \n', product_cat)

#Then I will be creating a frequency table for the Payment Method column
payment_frequency = df['Payment Method'].value_counts()
print('This is the frequency table for the Payment Method column: \n', payment_frequency)

#Then I will be creating a frequency table for the Payment Method column
Age_frequency = df['Customer Age Group'].value_counts()
print('This is the frequency table for the Payment Method column: \n', Age_frequency)
#A bar chart showing sales per product category.
SalesPerProduct = df.groupby('Product Category')['Total Sale Amount'].count().reset_index()
#grouping the coulumns in order tp produce a graph the represents sales per category

plt.figure(figsize=(7,6))
plt.bar(SalesPerProduct['Product Category'],
        SalesPerProduct['Total Sale Amount'],color = 'purple' )

#labeling the grapfh for better understanding and visualization. 
plt.title('Total Sales Per Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Amount of Sales')
  
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#A pie chart showing payment method distribution.
plt.figure(figsize=(10,15))
plt.pie(payment_frequency, labels = payment_frequency.index,
        autopct='%1.1f%%')#shows the percentages , and shows the portion in the pie chart
plt.title('The Payment Method Distribution')
plt.show()


#A scatter plot comparing customer age vs. total amount spent.
#Making a scatter plot using seaborn
import seaborn as sns
from pandas.api.types import CategoricalDtype

#arranging the age groups in ascending order
Ordered_Age = CategoricalDtype(categories=  ["18-25", "26-35", "36-45", "46-60", "60+"]
                               ,ordered= True)
df['Customer Age Group'] =df['Customer Age Group'].astype(Ordered_Age)

sns.scatterplot(x='Customer Age Group', y ='Total Sale Amount', hue='Total Sale Amount',size='Total Sale Amount', data=df)
plt.legend(bbox_to_anchor=(1,1.5),loc='best') # adding the legend to the best possible spot
plt.show()

#A line chart showing monthly total sales trends.
# Extract month number and convert to string
df['Month'] = df['Date of Purchase'].dt.month.astype(str)

#  Map month numbers of months to the name of the month using a dictionary
month_map = {
    '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec',
    '1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr',
    '5': 'May', '6': 'Jun', '7': 'Jul', '8': 'Aug'
}
df['Month Name'] = df['Month'].map(month_map)

#Ensuring that the data is represented in a timely order (Sep 2024 to Aug 2025)
month_order = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
month_cat_type = CategoricalDtype(categories=month_order, ordered=True)
df['Month Name'] = df['Month Name'].astype(month_cat_type)

# Grouping by month and sum sales
monthly_sales = df.groupby('Month Name')['Total Sale Amount'].sum().reset_index()

# Plot the graph
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(x='Month Name', y='Total Sale Amount', data=monthly_sales, marker='o', color='purple')

plt.title('Monthly Total Sales Trends (Sep 2024 – Aug 2025)', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Total Sale Amount (R)')
plt.tight_layout()
plt.show()

# saves randomized file as a csv file excluding the index as a column
df.to_csv("SLG Final Sales 2nd Save.csv", index=False)
df = pd.read_csv("SLG Final Sales 2nd Save.csv")



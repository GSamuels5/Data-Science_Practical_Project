# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 11:47:13 2025
 
@author: Luche Louw
@author: Ghamzah Samuels
@author: Shuaib Boolay
"""

import pandas as pd
df = pd.read_csv('C:/Users/SoftwareDeveloper3/Documents/Practical Modules/Group project/lewis_furniture_sales.csv')

 
df=df.drop_duplicates()
df.dropna()
print(df.isnull().sum())
 
print(df.head())
print(df.describe())
print(df.info())


#Revenue Analysis (15 marks)
#a. Find the top 5 products by revenue and the bottom 3 products by revenue.
top_5 = df.groupby('Product Name')["Total Sale Amount (R)"].sum().sort_values(ascending=False)
top_items = top_5.head(5)
bottom_3 = top_5.tail(3)
print("This is the top 5 products by revenue :\n", top_items)
print("This is the bottom 3  products by revenue :\n",bottom_3)

# b. Display the results in both dictionary format (product: revenue) and a horizontal bar chart.
Top_5 = top_items.to_dict()
Bottom_3 = bottom_3.to_dict()
print("This is my top 5 in dictionary format :\n", Top_5)
print("This is my bottom 3 in dictionary format :\n", Bottom_3)

import matplotlib.pyplot as plt
#Horizontal bar graph for top 5 products by revenue
# Combine top 5 and bottom 3 into one Series
combined = pd.concat([top_items, bottom_3])

# Create color list: red for top 5, green for bottom 3
colors = ["green"] * len(top_items) + ["red"] * len(bottom_3)

# Horizontal bar graph for combined products
plt.figure(figsize=(10, 8))
combined.plot(kind='barh', color=colors)

plt.xlabel("Total Revenue (R)")
plt.ylabel("Products")
plt.title("Top 5 vs Bottom 3 Products by Revenue")

# Put highest revenue item at the top
plt.gca().invert_yaxis()

plt.show()

#c. Which product category contributed the most to total store revenue?
Top_cat = df.groupby('Product Category')['Total Sale Amount (R)'].max().sort_values(ascending=False)
print("The product catergory with the most revenue: \n", Top_cat.head(1))

#---------------------------------------------------------------------------------------------------------------------------------
#question 4.2
#a) Calculate average spend per customer age group.

AverageSpent = df.groupby('Customer Age Group')['Total Sale Amount (R)'].sum().sort_values(ascending=False)
print(f"\nThe average spent per customer age group is:\n{AverageSpent}" )

#b) Using a dictionary, map each age group to their preferred payment method (most frequently used).

preferred_payment = df.groupby('Customer Age Group')['Payment Method'].agg(lambda x :x.mode()[0])# Lambda allowes you to define a function with one input and produces its output
preferred_payment = preferred_payment.to_dict()
print('The preferred payment method by age group is :' , preferred_payment)

#c) Which age group generates the highest average transaction value?
top_agegroup= AverageSpent.idxmax()
top_amount=AverageSpent.max()
print ('The age group that generated the highest average transaction value is', top_agegroup,' and they spent a total of ',top_amount)
#---------------------------------------------------------------------------------------------------------------------------------
#Quetion 4.3
#a) Group sales data by month and calculate ,Group sales data by month and calculate, 
#and Average sales per transaction per month

df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'], errors='coerce')
df['Month Num'] = df['Date of Purchase'].dt.month # converting full date to month
df['Month Name'] = df['Date of Purchase'].dt.strftime('%b')#indicatind that month will bea string

SalesbyMonth = df.groupby('Month Num')['Total Sale Amount (R)'].sum() #grouping the month by the sales and adding it
print("This is sales per month : ", SalesbyMonth)

# Count transactions per month
TransactionsPerMonth = df.groupby('Month Num')['Transaction ID'].count()
# Average sale per transaction per month
AvgPerTransaction = SalesbyMonth / TransactionsPerMonth
print("this is the average per transaction:", AvgPerTransaction)

# Get month labels in order , to track seasonal changes
month_labels = df.groupby('Month Num')['Month Name'].first()

#------------------------------------------------------------
#4.3b)Use a line graph with dual axes (left = total sales, right = average sales).
import matplotlib.pyplot as plt

Months = df['Month Name']

fig, ax1 = plt.subplots(figsize=(12,6))
# Making the Left y-axis Total Sales
ax1.plot(month_labels, SalesbyMonth.values, marker='s', color='red', label='Total Sales')
ax1.set_xlabel('Month')
ax1.set_ylabel('Total Sales (R)', color='red')
ax1.tick_params(axis='y', labelcolor='red')

#Making the Right y-axis: Average Sale per Transaction
#creating a second y axis
ax2 = ax1.twinx()
ax2.plot(month_labels, AvgPerTransaction.values, marker='o', color='orange', label='Average Sale per Transaction')
ax2.set_ylabel('Average Sale per Transaction (R)', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

#Creating more labels for better visualization
plt.title('Monthly Sales Analysis (Total vs Average per Transaction)')
ax1.grid(True)
fig.tight_layout()
plt.show()

# ===============================
# 4.4 Profit & Margin Analysis
# ===============================

# a.)
multi_map = {
    "Bedroom": 0.65, 
    "Living Room": 0.60, 
    "Dining": 0.55, 
    "Appliances": 0.70, 
    "Electronics": 0.75, 
    "Décor": 0.50
    }

multiplier = df["Product Category"].map(multi_map)
df["Profit"] = df["Total Sale Amount (R)"] * (1 - multiplier)

# b.)
cat_profit = df.groupby("Product Category")["Profit"].sum().reset_index()
cat_profit["Product Category Revenue"] = cat_profit["Product Category"].map(Top_cat)
cat_profit = cat_profit.sort_values(by="Profit", ascending=False)
print(f"\nThe Profit generated from each Product Category:\n{cat_profit}")
print(f"\nThe Revenue generated from each Product Category:\n{Top_cat}")

# c.)
print(f"\nThe Product Category which generated the most Revenue:\n{Top_cat.head(1)}")
print(f"\nHowever the Product Category which generated the most Profit:\n{cat_profit.head(1)}")
print("\n'Bedroom' Product Category generated the most Revenue for Lewis because it was baught at a higher quantity than the rest of the Product Categories, however 'Appliances' generated the most Profit becuase profit is calculated by total revenue - exspenses, it simply means that the exspenses for 'Bedroom' Category is alot more than 'Appliances' Category")
print("Meaning it cost Lewis alot of money to stock Products for 'Bedroom' Category")

# ========================================
# 4.5  Customer Loyalty & Repeat Purchases 
# ========================================

# a.)
uni_cus = df["Customer ID"].nunique()
print(f"\nThe Amount of unique customers in the dataset are:\n{uni_cus}")

# b.)
top_5_cus = df.groupby("Customer ID")["Total Sale Amount (R)"].sum()
print(f"\nTop 5 customers by total spent\n{top_5_cus.head()}")

# c.)
multi_pur_cus = len(df) - uni_cus
multi_pur_cus2 = multi_pur_cus/len(df) * 100
print(f"\n The percentage of customers who made 2 or more purchases:\n{multi_pur_cus2}%")

# d.)
print("\nLook at the customers that have purchased more than once at the store and offer them in store credit, a complementary gift card or 15% off their next purchase.")
print("And for the customers that haven't returned to our store we can introduce a loyalty point system to get them to want to return.")

# ========================================
# 4.6 Predictive Insight Challenge
# ========================================

import numpy as np


#Group revelant columns
grouped = df.groupby("Product Category")['Total Sale Amount (R)']

#turning the dataframe into a numerical array and extracting electronics
eft = grouped.get_group("Electronics").to_numpy()
#Mean
mean_val = np.mean(eft)
print(f"This is the Mean of the Electronics:  {mean_val:.2f}")

#Median
median_val = np.median(eft)
print(f"This is the Median of the Electronics:  {median_val:.2f}")

#Standard Deviation of transaction amounts
std_val = np.std(eft)
print(f"This is the Standard of the Electronics:  {std_val:.2f}")

#.B Based on this distribution, predict whether Electronics sales are more volatile than other categories.
print(f"Since the standard deviation({std_val:.2f}) is high and close to the mean ( {mean_val:.2f})then that means the Electronic sales are relatively volatile compared to the other sales.")

# C. Suggest how Lewis Furniture could reduce volatility in sales (e.g., discounts, bundles, loyalty programs).
print("Lewis can give a a discount on electronics when customers buy more than two electronic products")
print("They can have raffle prizes to win in months when electtronics prices was low and they must buy an electronic product.")
print("More loyalty points given to customers who buy electronics which is priced over 10K ")


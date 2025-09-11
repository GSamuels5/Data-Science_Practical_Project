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
plt.figure(figsize=(8, 9))
top_items.plot(kind='barh', color="red")
plt.xlabel("Total Revenue")
plt.ylabel("Products")
plt.title("This is the top 5 Products by Revenue")

plt.gca().invert_yaxis()#moves the top product on top
plt.show
#Horizontal bar graph for bottom 3 products by revenue
plt.figure(figsize=(8, 9))
bottom_3.plot(kind='barh', color="green")
plt.xlabel("Total Revenue")
plt.ylabel("Products")
plt.title("This is the top 5 Products by Revenue")
plt.gca().invert_yaxis()
plt.show

#c. Which product category contributed the most to total store revenue?
Top_cat = df.groupby('Product Category')['Total Sale Amount (R)'].max().sort_values(ascending=False)
print("The product catergory with the most revenue: \n", Top_cat.head(1))



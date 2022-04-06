import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import streamlit as st
import plotly.express as px
color = sns.color_palette()

df = pd.read_csv('data.csv' , encoding = 'ISO-8859-1')
# change the column names
df.rename(index=str, columns={'InvoiceNo': 'invoice_num',
                              'StockCode' : 'stock_code',
                              'Description' : 'description',
                              'Quantity' : 'quantity',
                              'InvoiceDate' : 'invoice_date',
                              'UnitPrice' : 'unit_price',
                              'CustomerID' : 'cust_id',
                              'Country' : 'country'}, inplace=True)

#Proses Data Cleaning
# check missing values for each column 
df.isnull().sum().sort_values(ascending=False)
# check out the rows with missing values
df[df.isnull().any(axis=1)].head()

# change the invoice_date format - String to Timestamp format
df['invoice_date'] = pd.to_datetime(df.invoice_date, format='%m/%d/%Y %H:%M')

# change description - UPPER case to LOWER case
df['description'] = df.description.str.lower()

st.write(df)

# df_new without missing values
df_new = df.dropna()

# check missing values for each column 
df_new.isnull().sum().sort_values(ascending=False)

# change columns type - String to Int type 
df_new['cust_id'] = df_new['cust_id'].astype('int64')
# Remove Quantity With Negative Value
df_new = df_new[df_new.quantity > 0]
# Menambahkan Column Amount Spent
df_new['amount_spent'] = df_new['quantity'] * df_new['unit_price']

# rearrange all the columns for easy reference
df_new = df_new[['invoice_num','invoice_date','stock_code',
'description','quantity','unit_price','amount_spent',
'cust_id','country']]
# Add the columns - Month, Day and Hour for the invoice
df_new.insert(loc=2, column='year_month', value=df_new['invoice_date'].map(lambda x: 100*x.year + x.month))
df_new.insert(loc=3, column='month', value=df_new.invoice_date.dt.month)
# +1 to make Monday=1.....until Sunday=7
df_new.insert(loc=4, column='day', value=(df_new.invoice_date.dt.dayofweek)+1)
df_new.insert(loc=5, column='hour', value=df_new.invoice_date.dt.hour)
st.write(df_new)

orders = df_new.groupby(by=['cust_id','country'], as_index=False)['invoice_num'].count()
bar_graph_orders = px.bar(orders, x='cust_id', y='invoice_num')
st.plotly_chart(bar_graph_orders)
st.header('The TOP 5 customers with most number of orders...')
top = orders.sort_values(by='invoice_num', ascending=False).head()
st.write(top)
st.header('How much money spent by the customers?')
money_spent = df_new.groupby(by=['cust_id','country'], as_index=False)['amount_spent'].sum()
bar_graph_moneyspent = px.bar(money_spent, x='cust_id', y='amount_spent')
st.plotly_chart(bar_graph_moneyspent)

st.header('The TOP 5 customers with highest money spent...')
moneyspentbycountry = money_spent.sort_values(by='amount_spent', ascending=False).head()
bar_top5_moneyspent = px.bar(moneyspentbycountry , x='cust_id' , y ='amount_spent' , color='country')
st.plotly_chart(bar_top5_moneyspent)
ax = df_new.groupby('invoice_num')['year_month'].value_counts().sort_index()
st.write(ax)







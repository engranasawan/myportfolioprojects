#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd


# In[2]:


path='C:/Users/engr-/Downloads/Compressed/archive'


# In[3]:


df_list=[]


# In[4]:


for filename in os.listdir(path):
    if filename.endswith('.csv'):
        df = pd.read_csv(os.path.join(path, filename))
        df_list.append(df)


# In[5]:


merged_df = pd.concat(df_list, ignore_index=True)


# In[2]:


data=pd.read_csv("C:\\Users\\engr-\\merged_dataset.csv")


# In[3]:


data.head()


# In[4]:


data.drop(['image','link','Unnamed: 0'],axis=1,inplace=True)


# In[5]:


data.head(10)


# In[6]:


# Find missing values in each column
missing_values = data.isnull().sum()


# In[7]:


print(missing_values)


# In[8]:


# Find the total number of rows
num_rows = data.shape[0]

print("Total number of rows: ", num_rows)


# In[9]:


data.head()


# In[10]:


# Drop rows with missing values
data = data.dropna(axis=0)


# In[11]:


# Find the total number of rows
num_rows = data.shape[0]

print("Total number of rows: ", num_rows)


# In[13]:


import matplotlib.pyplot as plt

# Count number of products in each main category
category_counts = data['main_category'].value_counts()

# Set colors for each category
colors = ['#3f9b0b', '#dd5f0d', '#2f5bb7', '#b72222', '#8e44ad', '#f39c12', '#c0392b']

# Plot a bar chart of the category counts
fig, ax = plt.subplots(figsize=(11,7))
bars = ax.bar(category_counts.index, category_counts.values, color=colors)

# Add category names and counts to the bars
for bar, category, count in zip(bars, category_counts.index, category_counts.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2, 
            f'{category}    {count}', ha='center', va='bottom', fontweight='bold', 
            fontsize=12, rotation=90)

# Customize plot aesthetics
ax.set_xlabel('Main Category')
ax.set_ylabel('Number of Products')
ax.set_title('Number of Products in Each Main Category', fontsize=16, fontweight='bold')
ax.tick_params(axis='both', which='both', length=0, labelsize=12)
ax.set_xticklabels([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()


# In[12]:


data['actual_price'] = data['actual_price'].str.replace('₹', '')
data['discount_price'] = data['discount_price'].str.replace('₹', '')


# In[13]:


data.head()


# In[14]:


print(data['actual_price'].dtype)
print(data['discount_price'].dtype)


# In[15]:


# Remove commas from actual_price and discount_price columns
data['actual_price'] = data['actual_price'].str.replace(',', '')
data['discount_price'] = data['discount_price'].str.replace(',', '')

# Convert actual_price and discount_price columns to float
data['actual_price'] = data['actual_price'].astype(float)
data['discount_price'] = data['discount_price'].astype(float)


# In[16]:


print(data['actual_price'].dtype)
print(data['discount_price'].dtype)


# In[17]:


data['discount_percent'] = (data['actual_price'] - data['discount_price']) / data['actual_price'] * 100


# In[33]:


# Create a histogram of discount percentages for each category
fig, ax = plt.subplots(figsize=(10,8))
for category in data['main_category'].unique():
    category_data = data[data['main_category'] == category]
    ax.hist(category_data['discount_percent'], bins=25, alpha=0.6, label=category)

# Customize plot aesthetics
ax.set_xlabel('Discount Percentage', fontsize=16)
ax.set_ylabel('Frequency', fontsize=16)
ax.set_title('Distribution of Discount Percentages by Category', fontsize=20, fontweight='bold')
ax.legend(fontsize=12)
ax.tick_params(axis='both', which='both', labelsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()


# In[40]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


# Calculate discount percentage
data['discount_percentage'] = (data['actual_price'] - data['discount_price']) / data['actual_price'] * 100

# Create a scatter plot showing the number of reviews and average rating for each product,
# with the size and color of the points representing the price of the product.
scatter = px.scatter(data, x='no_of_ratings', y='ratings', color='actual_price', size='discount_percentage',
                  hover_data=['name', 'main_category', 'sub_category', 'actual_price', 'discount_price'])

# Create a bar chart showing the number of products in each main category
bar = px.bar(data, x='main_category', color='main_category', 
              title='Number of Products in Each Main Category',
              labels={'main_category': 'Main Category', 'count()': 'Number of Products'},
              height=400)
bar.update_layout(showlegend=False)

# Create a histogram showing the distribution of actual prices
histogram = px.histogram(data, x='actual_price', nbins=30, color_discrete_sequence=['#636EFA'])

# Create a pie chart showing the proportion of products in each sub-category
pie = px.pie(data, names='sub_category', color_discrete_sequence=px.colors.qualitative.Set3,
              title='Proportion of Products in Each Sub-Category')

# Define the layout of the dashboard
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Product Dashboard'),
    html.Div([
        dcc.Graph(figure=scatter)
    ]),
    html.Div([
        dcc.Graph(figure=bar)
    ]),
    html.Div([
        dcc.Graph(figure=histogram)
    ]),
    html.Div([
        dcc.Graph(figure=pie)
    ])
])

# Run the dashboard
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:


app.run_server(port=8080)


# In[20]:


data.to_csv('amazon_sales_data_cleaned',index=False)


# In[ ]:


exit


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[1]:


import plotly.express as px
import matplotlib.pyplot as plt

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from tqdm import tqdm


# In[2]:


df = pd.read_json("../Downloads/txn_history-2021-10-07.jsonl", lines=True)
len(df)


# In[4]:


df['date'] = pd.to_datetime(df.date)


# In[5]:


df.columns


# In[6]:


df = df[["txn_type", "date", "eth", "punk_id", "type", "accessories"]]
df.head()


# In[7]:


df = df.explode("type")
df.head()


# In[8]:


fig = px.bar(df.drop_duplicates("punk_id")['type'].value_counts().rename_axis('type').reset_index(name='counts'),
             x="type", y="counts", color="type", title="Cryptopunk Type Counts")
fig.show()


# In[9]:


df.eth.describe()


# In[10]:


median_price = {}
i = 0
all_txns = []
punk_types = df.type.unique()
dates = sorted(df.date.unique())
prev_date = None
for date in tqdm(dates):
    if prev_date:
        df_up_to = df[(df.date <= date) & (df.date > prev_date)]
    else:
        # this only occurs for the first date!
        df_up_to = df[(df.date <= date)]

    median_price = df_up_to[df.txn_type == "Sold"].groupby("type").agg({"eth": "median"})['eth'].to_dict()
    for punk_type in punk_types:
        if punk_type not in median_price:
            # no median price/sales, so we include all transactions
            all_txns.append(df_up_to[df_up_to.type == punk_type])
        else:
            # only include transactions that are within at least 10% of the median price
            all_txns.append(df_up_to[(df_up_to.type == punk_type) & (df.eth >= median_price[punk_type] * .1)])

    prev_date = date
    
df = pd.concat(all_txns)


# In[11]:


len(df)


# In[12]:


df = df.drop_duplicates(["txn_type", "date", "eth", "punk_id", "type"])
len(df)


# In[13]:


max_sold = df[df.txn_type == "Sold"].eth.max()

# include all transactions with offers/bids up to 1.5x larger than largest sale
df = df[df.eth <= max_sold * 1.5 ]


# In[14]:


fig = px.histogram(df, x="eth", title="All Transaction ETH Prices")
fig.show()


# In[15]:


dates = df['date'].value_counts().sort_index().rename_axis('date').reset_index(name='counts')
plt.figure(figsize=(20,10))
plt.bar(dates['date'], dates['counts'], label="All Transactions")
plt.legend()
plt.xticks(rotation=60)
plt.ylim(0, 1000)
plt.title("Transactions per Day")
plt.ylabel("Number of Transactions")
plt.xlabel("Date")
plt.show()


# In[16]:


fig = px.bar(df[df.txn_type == 'Sold'].groupby("type").agg({"eth": "max"}).sort_values(by="eth").reset_index('type'),
             x="type", y="eth", color="type", title="CryptoPunk Max Sold Price by Type")
fig.show()


# In[17]:


human = df[(df.txn_type == 'Sold') & ((df.type == "Female") | (df.type == "Male")) ].groupby("date").agg({"eth": ["median"]}).reset_index("date")
alien = df[(df.txn_type == 'Sold') & ((df.type == "Alien")) ].groupby("date").agg({"eth": ["median"]}).reset_index("date")
zombie = df[(df.txn_type == 'Sold') & ((df.type == "Zombie")) ].groupby("date").agg({"eth": ["median"]}).reset_index("date")
ape = df[(df.txn_type == 'Sold') & ((df.type == "Ape")) ].groupby("date").agg({"eth": ["median"]}).reset_index("date")
plt.figure(figsize=(20,10))
plt.plot(human['date'], human['eth']['median'], label="Human Median Eth")
plt.plot(alien['date'], alien['eth']['median'], label="Alien Median Eth")
plt.plot(zombie['date'], zombie['eth']['median'], label="Zombie Median Eth")
plt.plot(ape['date'], ape['eth']['median'], label="Ape Median Eth")
plt.legend()
plt.xticks(rotation=60)
plt.title("Median Eth Price for Punks Sold Over Time by Type")
plt.show()


# In[18]:


df['num_attributes'] = df.accessories.apply(lambda x: len(x))


# In[19]:


fig = px.bar(df.drop_duplicates("punk_id")['num_attributes'].value_counts().rename_axis('num_attributes').reset_index(name='counts'),
             x="num_attributes", y="counts", color="num_attributes", title="Cryptopunk Distribution of Number of Attributes")
fig.show()


# In[20]:


# here are the actual counts
df.drop_duplicates("punk_id")['num_attributes'].value_counts()


# In[21]:


fig = px.bar(df[(df.txn_type == "Sold") & ((df.type == "Female") | (df.type == "Male"))].groupby("num_attributes").agg({"eth": "mean"}).reset_index("num_attributes"),
             x="num_attributes", y="eth", color="eth", title="Cryptopunk Price per Number of Attributes of Human Punks Only")
fig.show()


# In[ ]:





# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[18]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import plotly.express as px
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[19]:


st.title('General NFT Trends')


# In[20]:


st.markdown('This part shows the basic NFT trends on **Solana** ecosystem. It is intended to provide an overview of the current market for NFTs in Solana.')


# In[5]:


st.markdown('In this section, we are gonna track the basic metrics registered on **NFT Solana Ecosystem** so far such as:') 
st.write('- NFT sales executed')
st.write('- NFT sales volume in SOL')
st.write('- Active NFT purchasers')
st.write('- Average NFT price')
st.write('')


# In[10]:


sql = f"""
SELECT 
    trunc(block_timestamp,'day') AS date, 
    count(distinct tx_id) AS transactions,
  sum(transactions) over (order by date) as cum_transactions,
  sum(sales_amount) as volume_of_sales,
  sum(volume_of_sales) over (order by date) as cum_volume_sales,
  avg(sales_amount) as avg_nft_price,
  avg(avg_nft_price) over (order by date) as cum_avg_price,
  count(purchaser) as users,
  sum(users) over (order by date) as cum_users
from solana.core.fact_nft_sales where date>=current_date-INTERVAL '1 MONTH'
group by 1
order by 1 asc
"""

sql2 = f"""
SELECT 
    trunc(block_timestamp,'week') AS date, 
    count(distinct tx_id) AS transactions,
  sum(transactions) over (order by date) as cum_transactions,
  sum(sales_amount) as volume_of_sales,
  sum(volume_of_sales) over (order by date) as cum_volume_sales,
  avg(sales_amount) as avg_nft_price,
  avg(avg_nft_price) over (order by date) as cum_avg_price,
  count(purchaser) as users,
  sum(users) over (order by date) as cum_users
from solana.core.fact_nft_sales where date>=current_date-INTERVAL '1 MONTH'
group by 1
order by 1 asc
"""

sql3 = f"""
SELECT 
    trunc(block_timestamp,'month') AS date, 
    count(distinct tx_id) AS transactions,
  sum(transactions) over (order by date) as cum_transactions,
  sum(sales_amount) as volume_of_sales,
  sum(volume_of_sales) over (order by date) as cum_volume_sales,
  avg(sales_amount) as avg_nft_price,
  avg(avg_nft_price) over (order by date) as cum_avg_price,
  count(purchaser) as users,
  sum(users) over (order by date) as cum_users
from solana.core.fact_nft_sales where date>=current_date-INTERVAL '2 MONTHS'
group by 1
order by 1 asc
"""


# In[11]:


st.experimental_memo(ttl=21600)
def compute(a):
    data=sdk.query(a)
    return data

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()
#st.subheader('Terra general activity metrics regarding transactions')
#st.markdown('In this first part, we can take a look at the main activity metrics on Terra, where it can be seen how the number of transactions done across the protocol, as well as some other metrics such as fees and TPS.')


# In[22]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['transactions'],
                name='# of sales',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_transactions'],
                name='# of sales',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily NFT sales',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily sales", secondary_y=False)
fig1.update_yaxes(title_text="Total sales", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['transactions'],
                name='# of sales',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_transactions'],
                name='# of sales',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly NFT sales',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly sales", secondary_y=False)
fig2.update_yaxes(title_text="Total sales", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['transactions'],
                name='# of sales',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_transactions'],
                name='# of sales',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly NFT sales',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly sales", secondary_y=False)
fig3.update_yaxes(title_text="Total sales", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily sales", "Weekly sales", "Monthly sales"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[15]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['volume_of_sales'],
                name='Volume in sales (SOL)',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_volume_sales'],
                name='Volume in sales (SOL)',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily NFT volume (SOL)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily volume (SOL)", secondary_y=False)
fig1.update_yaxes(title_text="Total volume (SOL)", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['volume_of_sales'],
                name='Volume in sales (SOL)',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_volume_sales'],
                name='Volume in sales (SOL)',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly NFT volume (SOL)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly volume (SOL)", secondary_y=False)
fig2.update_yaxes(title_text="Total volume (SOL)", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['volume_of_sales'],
                name='Volume in sales (SOL)',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_volume_sales'],
                name='Volume in sales (SOL)',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly NFT volume (SOL)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly volume (SOL)", secondary_y=False)
fig3.update_yaxes(title_text="Total volume (SOL)", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily volume", "Weekly volume", "Monthly volume"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[16]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['users'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_users'],
                name='# of users',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily NFT purchasers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily users", secondary_y=False)
fig1.update_yaxes(title_text="Total users", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['users'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_users'],
                name='# of users',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly NFT purchasers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly users", secondary_y=False)
fig2.update_yaxes(title_text="Total users", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['users'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_users'],
                name='# of users',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly NFT purchasers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly users", secondary_y=False)
fig3.update_yaxes(title_text="Total users", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily purchasers", "Weekly purchasers", "Monthly purchasers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[17]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Line(x=df['date'],
                y=df['avg_nft_price'],
                name='Price (SOL)',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y'))

fig1.update_layout(
    title='Daily NFT average price',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily average price (SOL)", secondary_y=False)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Line(x=df['date'],
                y=df2['avg_nft_price'],
                name='Price (SOL)',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y'))

fig2.update_layout(
    title='Weekly NFT average price',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly average price (SOL)", secondary_y=False)

# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Line(x=df['date'],
                y=df3['avg_nft_price'],
                name='Price (SOL)',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y'))

fig3.update_layout(
    title='Monthly NFT average price',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly average price (SOL)", secondary_y=False)


tab1, tab2, tab3 = st.tabs(["Daily average NFT price", "Weekly average NFT price", "Monthly average NFT price"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


st.title('Marketplaces Competition')


# In[3]:


st.markdown('This part shows the basic NFT trends on **Solana** ecosystem represented by marketplace. It is intended to provide an overview of the current market for NFTs in Solana on each available NFT marketplace.')


# In[4]:


st.markdown('In this section, we are gonna track the basic metrics registered on **NFT Solana Ecosystem** so far such as:') 
st.write('- NFT sales executed')
st.write('- NFT sales volume in SOL')
st.write('- Active NFT purchasers')
st.write('- Average NFT price')
st.write('')


# In[5]:


sql = f"""
SELECT 
    trunc(block_timestamp,'day') AS date, 
  case when marketplace='solana monkey business marketplace' then 'SMB market' else marketplace end as secondary_market,
    count(distinct tx_id) AS transactions,
  sum(transactions) over (partition by secondary_market order by date) as cum_transactions,
  sum(sales_amount) as volume_of_sales,
  sum(volume_of_sales) over (partition by secondary_market order by date) as cum_volume_sales,
  avg(sales_amount) as avg_nft_price,
  avg(avg_nft_price) over (partition by secondary_market order by date) as cum_avg_price,
  count(purchaser) as users,
  sum(users) over (partition by secondary_market order by date) as cum_users
from solana.core.fact_nft_sales where date>=current_date-INTERVAL '1 MONTH'
group by 1,2
order by 1 asc
"""

sql2 = f"""
SELECT 
    trunc(block_timestamp,'week') AS date, 
  case when marketplace='solana monkey business marketplace' then 'SMB market' else marketplace end as secondary_market,
    count(distinct tx_id) AS transactions,
  sum(transactions) over (partition by secondary_market order by date) as cum_transactions,
  sum(sales_amount) as volume_of_sales,
  sum(volume_of_sales) over (partition by secondary_market order by date) as cum_volume_sales,
  avg(sales_amount) as avg_nft_price,
  avg(avg_nft_price) over (partition by secondary_market order by date) as cum_avg_price,
  count(purchaser) as users,
  sum(users) over (partition by secondary_market order by date) as cum_users
from solana.core.fact_nft_sales where date>=current_date-INTERVAL '1 MONTH'
group by 1,2
order by 1 asc
"""

sql3 = f"""
SELECT 
    trunc(block_timestamp,'month') AS date, 
  case when marketplace='solana monkey business marketplace' then 'SMB market' else marketplace end as secondary_market,
    count(distinct tx_id) AS transactions,
  sum(transactions) over (partition by secondary_market order by date) as cum_transactions,
  sum(sales_amount) as volume_of_sales,
  sum(volume_of_sales) over (partition by secondary_market order by date) as cum_volume_sales,
  avg(sales_amount) as avg_nft_price,
  avg(avg_nft_price) over (partition by secondary_market order by date) as cum_avg_price,
  count(purchaser) as users,
  sum(users) over (partition by secondary_market order by date) as cum_users
from solana.core.fact_nft_sales where date>=current_date-INTERVAL '2 MONTHS'
group by 1,2
order by 1 asc
"""


# In[6]:


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


# In[14]:


import plotly.express as px

fig1 = px.line(df, x="date", y="transactions", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Vivid)
fig1.update_layout(
    title='Daily NFT sales by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.line(df2, x="date", y="transactions", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Vivid)
fig2.update_layout(
    title='Weekly NFT sales by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.line(df3, x="date", y="transactions", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Vivid)
fig3.update_layout(
    title='Monthly NFT sales by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily sales by marketplace", "Weekly sales by marketplace", "Monthly sales by marketplace"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[7]:


import plotly.express as px

fig1 = px.line(df, x="date", y="cum_transactions", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Vivid)
fig1.update_layout(
    title='Daily total NFT sales by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.line(df2, x="date", y="cum_transactions", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Vivid)
fig2.update_layout(
    title='Weekly total NFT sales by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.line(df3, x="date", y="cum_transactions", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Vivid)
fig3.update_layout(
    title='Monthly total NFT sales by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily total sales", "Weekly total sales", "Monthly total sales"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[9]:


import plotly.express as px

fig1 = px.area(df, x="date", y="volume_of_sales", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Safe)
fig1.update_layout(
    title='Daily NFT volume (SOL) by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.area(df2, x="date", y="volume_of_sales", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Safe)
fig2.update_layout(
    title='Weekly NFT volume (SOL) by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.area(df3, x="date", y="volume_of_sales", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Safe)
fig3.update_layout(
    title='Monthly NFT volume (SOL) by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily volume by marketplace", "Weekly volume by marketplace", "Monthly volume by marketplace"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[10]:


import plotly.express as px

fig1 = px.area(df, x="date", y="cum_volume_sales", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Safe)
fig1.update_layout(
    title='Daily total volume (SOL) by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.area(df2, x="date", y="cum_volume_sales", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Safe)
fig2.update_layout(
    title='Weekly total volume (SOL) by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.area(df3, x="date", y="cum_volume_sales", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Safe)
fig3.update_layout(
    title='Monthly total volume (SOL) by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily total volume", "Weekly total volume", "Monthly total volume"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[11]:


import plotly.express as px

fig1 = px.bar(df, x="date", y="users", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Plotly)
fig1.update_layout(
    title='Daily NFT purchasers by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.bar(df2, x="date", y="users", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Plotly)
fig2.update_layout(
    title='Weekly NFT purchasers by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.bar(df3, x="date", y="users", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Monthly NFT purchasers by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily purchasers by marketplace", "Weekly purchasers by marketplace", "Monthly purchasers by marketplace"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[12]:


import plotly.express as px

fig1 = px.bar(df, x="date", y="cum_users", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Plotly)
fig1.update_layout(
    title='Daily total purchasers by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.bar(df2, x="date", y="cum_users", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Plotly)
fig2.update_layout(
    title='Weekly total purchasers by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.bar(df3, x="date", y="cum_users", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Monthly total purchasers by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily total purchasers", "Weekly total purchasers", "Monthly total purchasers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[13]:


import plotly.express as px

fig1 = px.line(df, x="date", y="avg_nft_price", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Light24)
fig1.update_layout(
    title='Daily average NFT price (SOL) by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.line(df2, x="date", y="avg_nft_price", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Light24)
fig2.update_layout(
    title='Weekly average NFT price (SOL) by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.line(df3, x="date", y="avg_nft_price", color="secondary_market", color_discrete_sequence=px.colors.qualitative.Light24)
fig3.update_layout(
    title='Monthly average NFT price (SOL) by marketplace',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily NFT price by marketplace", "Weekly NFT price by marketplace", "Monthly NFT price by marketplace"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[ ]:





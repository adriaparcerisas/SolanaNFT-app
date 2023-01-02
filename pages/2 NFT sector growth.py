#!/usr/bin/env python
# coding: utf-8

# In[20]:


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


# In[21]:


st.title('NFT sector growth in Solana Ecosystem')


# In[22]:


st.markdown('This part shows the basic NFT growth on **Solana** ecosystem. It is intended to provide an overview of the growth evolution of Solana NFT activity.')


# In[23]:


st.markdown('In this section, we are gonna track the following NFT metrics:') 
st.write('- Total NFT mints and growth rate over time')
st.write('- Total sales and growth rate over time')
st.write('- Total minters and growth rate over time')
st.write('- Total NFT purchasers and growth rate over time')
st.write('')


# In[24]:


sql = f"""
--Create a series of dashboards that tracks the following metrics with Solana NFTs: 
  ---Total mints and growth rates of mints over time 
  --Total NFT sales and growth rates of sales over time 
  --Total unique wallets that have minted or purchased a Solana NFT and growth rates over time 
  --Total Unique Signers of Metaplex programs 
  --Total minters of NFTs using Candy Machine V1 and total minters of NFTs using Candy Machine V2 
 -- -Total users of Metaplex's Auction House program
with 
  mints as (
  select 
  trunc(block_timestamp,'day') as date,
count(distinct tx_id) as mints,
  sum(mints) over (order by date) as total_mints,
--count(distinct y.tx_id) as sales,
count(distinct purchaser ) as minters,
  sum(minters) over (order by date) as total_minters
--count(distinct y.purchaser) as purchasers
from solana.core.fact_nft_mints --x, solana.core.fact_nft_sales y where trunc(x.block_timestamp,'day')=trunc(y.block_timestamp,'day')
group by 1
order by 1
  ),
  sales as (
  select 
  trunc(block_timestamp,'day') as date,
--count(distinct x.tx_id) as mints,
count(distinct tx_id) as sales,
  sum(sales) over (order by date) as total_sales,
--count(distinct x.purchaser ) as minters,
count(distinct purchaser) as purchasers,
  sum(purchasers) over (order by date) as total_purchasers
from solana.core.fact_nft_sales --y where trunc(x.block_timestamp,'day')=trunc(y.block_timestamp,'day')
group by 1
order by 1
),
  final_data as (
SELECT
  x.date,
total_mints,
  lag(total_mints,1) over (order by x.date) as lasts,
  case when lasts=0 then 0 else (total_mints-lasts)/lasts end as mints_growth_rate,
total_sales,
lag(total_sales,1) over (order by x.date) as lasts2,
  case when lasts2=0 then 0 else (total_sales-lasts2)/lasts2 end as sales_growth_rate,  
total_minters,
 lag(total_minters,1) over (order by x.date) as lasts3,
  case when lasts3=0 then 0 else (total_minters-lasts3)/lasts3 end as minters_growth_rate, 
total_purchasers,
 lag(total_purchasers,1) over (order by x.date) as lasts4,
  case when lasts4=0 then 0 else (total_purchasers-lasts4)/lasts4 end as purchasers_growth_rate
from mints x
  left join sales y on x.date=y.date 
order by 1 asc
  )
SELECT
date,
total_mints, sum(mints_growth_rate) over (order by date) as mints_growth_rate,
total_sales, sum(sales_growth_rate) over (order by date) as sales_growth_rate,
total_minters, sum(minters_growth_rate) over (order by date) as minters_growth_rate,
total_purchasers, sum(purchasers_growth_rate) over (order by date) as purchasers_growth_rate
from final_data
order by 1 asc
"""

sql2 = f"""
--Create a series of dashboards that tracks the following metrics with Solana NFTs: 
  ---Total mints and growth rates of mints over time 
  --Total NFT sales and growth rates of sales over time 
  --Total unique wallets that have minted or purchased a Solana NFT and growth rates over time 
  --Total Unique Signers of Metaplex programs 
  --Total minters of NFTs using Candy Machine V1 and total minters of NFTs using Candy Machine V2 
 -- -Total users of Metaplex's Auction House program
with 
  mints as (
  select 
  trunc(block_timestamp,'week') as date,
count(distinct tx_id) as mints,
  sum(mints) over (order by date) as total_mints,
--count(distinct y.tx_id) as sales,
count(distinct purchaser ) as minters,
  sum(minters) over (order by date) as total_minters
--count(distinct y.purchaser) as purchasers
from solana.core.fact_nft_mints --x, solana.core.fact_nft_sales y where trunc(x.block_timestamp,'day')=trunc(y.block_timestamp,'day')
group by 1
order by 1
  ),
  sales as (
  select 
  trunc(block_timestamp,'week') as date,
--count(distinct x.tx_id) as mints,
count(distinct tx_id) as sales,
  sum(sales) over (order by date) as total_sales,
--count(distinct x.purchaser ) as minters,
count(distinct purchaser) as purchasers,
  sum(purchasers) over (order by date) as total_purchasers
from solana.core.fact_nft_sales --y where trunc(x.block_timestamp,'day')=trunc(y.block_timestamp,'day')
group by 1
order by 1
),
  final_data as (
SELECT
  x.date,
total_mints,
  lag(total_mints,1) over (order by x.date) as lasts,
  case when lasts=0 then 0 else (total_mints-lasts)/lasts end as mints_growth_rate,
total_sales,
lag(total_sales,1) over (order by x.date) as lasts2,
  case when lasts2=0 then 0 else (total_sales-lasts2)/lasts2 end as sales_growth_rate,  
total_minters,
 lag(total_minters,1) over (order by x.date) as lasts3,
  case when lasts3=0 then 0 else (total_minters-lasts3)/lasts3 end as minters_growth_rate, 
total_purchasers,
 lag(total_purchasers,1) over (order by x.date) as lasts4,
  case when lasts4=0 then 0 else (total_purchasers-lasts4)/lasts4 end as purchasers_growth_rate
from mints x
  left join sales y on x.date=y.date 
order by 1 asc
  )
SELECT
date,
total_mints, sum(mints_growth_rate) over (order by date) as mints_growth_rate,
total_sales, sum(sales_growth_rate) over (order by date) as sales_growth_rate,
total_minters, sum(minters_growth_rate) over (order by date) as minters_growth_rate,
total_purchasers, sum(purchasers_growth_rate) over (order by date) as purchasers_growth_rate
from final_data
order by 1 asc
"""

sql3 = f"""
--Create a series of dashboards that tracks the following metrics with Solana NFTs: 
  ---Total mints and growth rates of mints over time 
  --Total NFT sales and growth rates of sales over time 
  --Total unique wallets that have minted or purchased a Solana NFT and growth rates over time 
  --Total Unique Signers of Metaplex programs 
  --Total minters of NFTs using Candy Machine V1 and total minters of NFTs using Candy Machine V2 
 -- -Total users of Metaplex's Auction House program
with 
  mints as (
  select 
  trunc(block_timestamp,'month') as date,
count(distinct tx_id) as mints,
  sum(mints) over (order by date) as total_mints,
--count(distinct y.tx_id) as sales,
count(distinct purchaser ) as minters,
  sum(minters) over (order by date) as total_minters
--count(distinct y.purchaser) as purchasers
from solana.core.fact_nft_mints --x, solana.core.fact_nft_sales y where trunc(x.block_timestamp,'day')=trunc(y.block_timestamp,'day')
group by 1
order by 1
  ),
  sales as (
  select 
  trunc(block_timestamp,'month') as date,
--count(distinct x.tx_id) as mints,
count(distinct tx_id) as sales,
  sum(sales) over (order by date) as total_sales,
--count(distinct x.purchaser ) as minters,
count(distinct purchaser) as purchasers,
  sum(purchasers) over (order by date) as total_purchasers
from solana.core.fact_nft_sales --y where trunc(x.block_timestamp,'day')=trunc(y.block_timestamp,'day')
group by 1
order by 1
),
  final_data as (
SELECT
  x.date,
total_mints,
  lag(total_mints,1) over (order by x.date) as lasts,
  case when lasts=0 then 0 else (total_mints-lasts)/lasts end as mints_growth_rate,
total_sales,
lag(total_sales,1) over (order by x.date) as lasts2,
  case when lasts2=0 then 0 else (total_sales-lasts2)/lasts2 end as sales_growth_rate,  
total_minters,
 lag(total_minters,1) over (order by x.date) as lasts3,
  case when lasts3=0 then 0 else (total_minters-lasts3)/lasts3 end as minters_growth_rate, 
total_purchasers,
 lag(total_purchasers,1) over (order by x.date) as lasts4,
  case when lasts4=0 then 0 else (total_purchasers-lasts4)/lasts4 end as purchasers_growth_rate
from mints x
  left join sales y on x.date=y.date 
order by 1 asc
  )
SELECT
date,
total_mints, sum(mints_growth_rate) over (order by date) as mints_growth_rate,
total_sales, sum(sales_growth_rate) over (order by date) as sales_growth_rate,
total_minters, sum(minters_growth_rate) over (order by date) as minters_growth_rate,
total_purchasers, sum(purchasers_growth_rate) over (order by date) as purchasers_growth_rate
from final_data
order by 1 asc
"""


# In[25]:


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


# In[26]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['total_mints'],
                name='# of mints',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['mints_growth_rate'],
                name='Rate',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily NFT mints growth',
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
fig1.update_yaxes(title_text="Daily mints", secondary_y=False)
fig1.update_yaxes(title_text="Total mints growth", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df2['date'],
                y=df2['total_mints'],
                name='# of mints',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['mints_growth_rate'],
                name='Rate',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly NFT mints growth',
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
fig2.update_yaxes(title_text="Weekly mints", secondary_y=False)
fig2.update_yaxes(title_text="Total mints growth", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df3['date'],
                y=df3['total_mints'],
                name='# of mints',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['mints_growth_rate'],
                name='Rate',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly NFT mints growth',
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
fig3.update_yaxes(title_text="Monthly mints", secondary_y=False)
fig3.update_yaxes(title_text="Total mints growth", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily mints growth", "Weekly mints growth", "Monthly mints growth"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[27]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['total_sales'],
                name='# of sales',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['sales_growth_rate'],
                name='Rate',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily NFT sales growth',
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
fig1.update_yaxes(title_text="Total sales growth", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df2['date'],
                y=df2['total_sales'],
                name='# of sales',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['sales_growth_rate'],
                name='Rate',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly NFT sales growth',
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
fig2.update_yaxes(title_text="Total sales growth", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df3['date'],
                y=df3['total_sales'],
                name='# of sales',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['sales_growth_rate'],
                name='Rate',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly NFT sales growth',
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
fig3.update_yaxes(title_text="Total sales growth", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily sales growth", "Weekly sales growth", "Monthly sales growth"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[28]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['total_minters'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['minters_growth_rate'],
                name='Rate',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily NFT minters',
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
fig1.update_yaxes(title_text="Total minters growth", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df2['date'],
                y=df2['total_minters'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['minters_growth_rate'],
                name="Rate",
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly NFT minters',
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
fig2.update_yaxes(title_text="Total minters growth", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df3['date'],
                y=df3['total_minters'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['minters_growth_rate'],
                name='# of users',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly NFT minters',
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
fig3.update_yaxes(title_text="Total minters growth", secondary_y=True)


tab1, tab2, tab3 = st.tabs(["Daily minters growth", "Weekly minters growth", "Monthly minters growth"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[29]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['total_purchasers'],
                name='# of users',
                marker_color='rgb(250, 147, 165)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['purchasers_growth_rate'],
                name='Rate',
                marker_color='rgb(225, 12, 48)'
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
fig1.update_yaxes(title_text="Total purchasers growth", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df2['date'],
                y=df2['total_purchasers'],
                name='# of users',
                marker_color='rgb(250, 147, 165)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['purchasers_growth_rate'],
                name='Rate',
                marker_color='rgb(225, 12, 48)'
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
fig2.update_yaxes(title_text="Total purchasers growth", secondary_y=True)

# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df3['date'],
                y=df3['total_purchasers'],
                name='# of users',
                marker_color='rgb(250, 147, 165)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['purchasers_growth_rate'],
                name='Rate',
                marker_color='rgb(225, 12, 48)'
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
fig3.update_yaxes(title_text="Total purchasers growth", secondary_y=True)


tab1, tab2, tab3 = st.tabs(["Daily purchasers growth", "Weekly purchasers growth", "Monthly purchasers growth"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[30]:


sql="""
SELECT
trunc(block_timestamp,'day') as date,
case when label_type='nft' then label_type else 'Others' end as type,
sum(1) as transactions,
sum(transactions) over (partition by type order by date) as cum_transactions
from solana.core.fact_events x
  join solana.core.dim_labels y on x.program_id=y.address
  where succeeded='TRUE' and block_timestamp>=CURRENT_DATE-INTERVAL '1 MONTH'
  group by 1,2
order by 1 asc 
"""


# In[31]:


st.write("")
st.markdown('In this last charts can be seen the evolution of NFT market share accross Solana ecosystem.')

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()


# In[32]:


import plotly.express as px

fig1 = px.area(df, x="date", y="transactions", color="type", color_discrete_sequence=px.colors.qualitative.Antique)
fig1.update_layout(
    title='Solana NFT events vs others over the past month',
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

import plotly.express as px

fig2 = px.area(df, x="date", y="cum_transactions", color="type", color_discrete_sequence=px.colors.qualitative.Antique)
fig2.update_layout(
    title='Cumulative NFT events vs others over the past month',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1, # gap between bars of the same location coordinate.
    barmode="stack"
)

col1,col2=st.columns(2)
with col1:
    st.plotly_chart(fig1, theme=None, use_container_width=True)
col2.plotly_chart(fig2, theme=None, use_container_width=True)


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[3]:


st.title('Collections trend')


# In[22]:


st.markdown('This last part shows a dive deep table about the NFT projects that are currently in the markets that work with Solana. There it can be seen concrete and interesting metrics such as total sales, total purchasers, volume moved, as well as 24h and 7-days percentage growth of each metric. Furthermore, the collections are catalogued as top tier, strong and common depending on their attributes. For the first group, a purple button is shown in the final of the collection name, for the second group is green and for the common group orange.') 


# In[24]:


sql = f"""
WITH 
  sales AS (
  SELECT
   block_timestamp, 
   block_id, 
   n.mint, 
   b.label, 
   succeeded, 
  n.sales_amount,n.seller,n.purchaser,
  marketplace,
  n.tx_id
FROM solana.core.fact_nft_sales n 
LEFT OUTER JOIN solana.core.dim_labels b
ON n.mint = b.address
WHERE label IS NOT NULL),
  final_data as (
SELECT 
    trunc(block_timestamp,'day') AS date, 
  label as collection,
    count(distinct tx_id) AS transactions,
  sum(transactions) over (partition by collection order by date) as cum_transactions,
  sum(sales_amount) as volume_of_sales,
  sum(volume_of_sales) over (partition by collection order by date) as cum_volume_sales,
  avg(sales_amount) as avg_nft_price,
  avg(avg_nft_price) over (partition by collection order by date) as cum_avg_price,
  count(purchaser) as users,
  sum(users) over (partition by collection order by date) as cum_users
from sales
group by 1,2
order by 1 asc
  ),
  final_data_2 as (
SELECT
date,
collection,
cum_transactions as total_transactions,
  LAG(cum_transactions,1) IGNORE NULLS OVER (partition by collection ORDER BY date) as prev_transactions,
((cum_transactions-prev_transactions)/cum_transactions)*100 as txs_24h_growth,
LAG(cum_transactions,7) IGNORE NULLS OVER (partition by collection ORDER BY date) as last_transactions,
((cum_transactions-last_transactions)/cum_transactions)*100 as txs_7d_growth,
cum_volume_sales as total_volume_sales,
  LAG(cum_volume_sales,1) IGNORE NULLS OVER (partition by collection ORDER BY date) as prev_volume,
((cum_volume_sales-prev_volume)/cum_volume_sales)*100 as volume_24h_growth,
LAG(cum_volume_sales,7) IGNORE NULLS OVER (partition by collection ORDER BY date) as last_volume,
((cum_volume_sales-last_volume)/cum_volume_sales)*100 as volume_7d_growth,
cum_avg_price as avg_nft_price,
cum_users as total_users,
rank() over (partition by date order by total_transactions desc) as rank
from final_data
order by date asc
  )
SELECT
case when rank <10 then concat(collection,' 🟪') 
  when rank between 10 and 100 then concat(collection,' 🟢')
    when rank between 100 and 1000 then concat(collection,' 🟠')
  else concat(collection,' 🔴')
  end as "NFT Collection",
total_transactions as "Total transactions",
txs_24h_growth as "24h transactions growth (%)",
txs_7d_growth as "7 days transactions growth (%)",
total_volume_sales "Total volume (SOL)",
volume_24h_growth as "24h volume growth (%)",
volume_7d_growth as "7d volume growth (%)",
avg_nft_price as "Average sales price",
total_users as "Total buyers"
from final_data_2 where date=current_date-1
order by 2 desc
"""

sql2="""
WITH 
  sales AS (
  SELECT
   block_timestamp, 
   block_id, 
   n.mint, 
   b.label, 
   succeeded, 
  n.sales_amount,n.seller,n.purchaser,
  marketplace,
  n.tx_id
FROM solana.core.fact_nft_sales n 
LEFT OUTER JOIN solana.core.dim_labels b
ON n.mint = b.address
WHERE label IS NOT NULL),
  final_data as (
SELECT 
    trunc(block_timestamp,'day') AS date, 
  label as collection,
    count(distinct tx_id) AS transactions,
  sum(transactions) over (partition by collection order by date) as cum_transactions,
  sum(sales_amount) as volume_of_sales,
  sum(volume_of_sales) over (partition by collection order by date) as cum_volume_sales,
  avg(sales_amount) as avg_nft_price,
  avg(avg_nft_price) over (partition by collection order by date) as cum_avg_price,
  count(purchaser) as users,
  sum(users) over (partition by collection order by date) as cum_users
from sales
group by 1,2
order by 1 asc
  ),
  final_data_2 as (
SELECT
date,
collection,
cum_transactions as total_transactions,
  LAG(cum_transactions,1) IGNORE NULLS OVER (partition by collection ORDER BY date) as prev_transactions,
((cum_transactions-prev_transactions)/cum_transactions)*100 as txs_24h_growth,
LAG(cum_transactions,7) IGNORE NULLS OVER (partition by collection ORDER BY date) as last_transactions,
((cum_transactions-last_transactions)/cum_transactions)*100 as txs_7d_growth,
cum_volume_sales as total_volume_sales,
  LAG(cum_volume_sales,1) IGNORE NULLS OVER (partition by collection ORDER BY date) as prev_volume,
((cum_volume_sales-prev_volume)/cum_volume_sales)*100 as volume_24h_growth,
LAG(cum_volume_sales,7) IGNORE NULLS OVER (partition by collection ORDER BY date) as last_volume,
((cum_volume_sales-last_volume)/cum_volume_sales)*100 as volume_7d_growth,
cum_avg_price as avg_nft_price,
cum_users as total_users,
rank() over (partition by date order by total_transactions desc) as rank
from final_data
order by date asc
  ),
  types as (
SELECT
case when rank <10 then '🟪 Stellar collections' 
  when rank between 10 and 100 then '🟢 Top tier collections'
    when rank between 100 and 1000 then '🟠 Common collections'
  else '🔴 Other collections'
  end as "NFT Collection",
total_transactions as "Total transactions",
txs_24h_growth as "24h transactions growth (%)",
txs_7d_growth as "7 days transactions growth (%)",
total_volume_sales "Total volume (SOL)",
volume_24h_growth as "24h volume growth (%)",
volume_7d_growth as "7d volume growth (%)",
avg_nft_price as "Average sales price",
total_users as "Total buyers"
from final_data_2
order by 2 desc
)
select
"NFT Collection" as types,
avg("Total 2023 transactions") as avg_total_transactions,
avg("24h transactions growth (%)") as avg_24h_growth_pcg,
sum("Total 2023 buyers") as total_buyers
from types group by 1 order by 2 desc 
"""


# In[25]:


st.experimental_memo(ttl=86400)
def compute(a):
    data=sdk.query(a)
    return data

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()


# In[23]:


st.dataframe(df)


# In[27]:


import plotly.graph_objects as go
fig1 = go.Figure([go.Bar(x=df2['types'], y=df2['avg_total_transactions'],marker_color=px.colors.qualitative.Plotly)])
fig1.update_layout(
    title='Average # of sales per collection group',
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

st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

fig3 = go.Figure([go.Bar(x=df2['types'], y=df2['total_buyers'],marker_color=px.colors.qualitative.Plotly)])
fig3.update_layout(
    title='Purchasers distribution per group',
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

st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


fig2 = px.violin(df, y="24h transactions growth (%)", box=True, # draw box plot inside the violin
                points='all', color_discrete_sequence=px.colors.qualitative.Plotly # can be 'outliers', or False
               )
fig2.update_layout(
    title='Violin plot about 24h NFT sales growth % on Solana',
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
st.plotly_chart(fig2, theme="streamlit", use_container_width=True)


# In[ ]:

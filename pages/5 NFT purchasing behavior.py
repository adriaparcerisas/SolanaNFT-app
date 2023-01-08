#!/usr/bin/env python
# coding: utf-8

# In[3]:


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


# In[4]:


st.title('NFT purchasing behavior')


# In[5]:


st.markdown('The user behavior on the major of the blockchains are different. The same occurs with the NFT purchases over the entire ecosystem. In this section we are gonna analyze the distribution of Solana NFT sales and the purchases above and below some specific prices to determine the trends.') 


# In[6]:


st.markdown('First of all, we will take a look at the distribution of both sales and purchasers by the price of the sales, and we will find some correlation between both metrics. The prices are grouped in different buckets such as:')
st.write('- Price above 500 SOL')
st.write('- Between 100 and 500 SOL')
st.write('- Between 10 and 50 SOL')
st.write('- Between 5 and 10 SOL')
st.write('- Between 2 and 5 SOL')
st.write('- Between 0.5 and 2 SOL')
st.write('- Below 0.5 SOL')
st.write('')


# In[7]:


sql = f"""
--Show the distribution of all Solana NFT sales on Solana. 
--What percentage of all sales have been above 1 SOL? Above 10 sol?
--How many unique wallets have made a NFT purchase that was above 10 SOL? Above 100 SOL?

SELECT
case when sales_amount >500 then 'a. >500 SOL'
  when sales_amount between 100 and 500 then 'b. 100-500 SOL'
  when sales_amount between 50 and 100 then 'c. 50-100 SOL'
  when sales_amount between 10 and 50 then 'd. 10-50 SOL'
  when sales_amount between 5 and 10 then 'e. 5-10 SOL'
  when sales_amount between 2 and 5 then 'f. 2-5 SOL'
  when sales_amount between 0.5 and 2 then 'g. 0.5-2 SOL'
  else 'h. <0.5 SOL' end as "Price Range",
  count(distinct tx_id) as "Number of sales",
  count(distinct purchaser) as "Number of purchasers"
from solana.fact_nft_sales 
group by 1
order by 1
"""

sql2 = f"""
--Show the distribution of all Solana NFT sales on Solana. 
--What percentage of all sales have been above 1 SOL? Above 10 sol?
--How many unique wallets have made a NFT purchase that was above 10 SOL? Above 100 SOL?
WITH
  table1 as (
  SELECT
  count(distinct tx_id) as all_sales
  from solana.fact_nft_sales
  ),
  table2 as (
SELECT
count(case when sales_amount >1 then 1 end) as n_sales_above_1,
count(case when sales_amount >10 then 1 end) as n_sales_above_10
from solana.fact_nft_sales
)
SELECT
all_sales as "Total Solana NFT sales",
n_sales_above_1 as "Sales above 1 SOL",
n_sales_above_10 as "Sales above 10 SOL",
(n_sales_above_1/all_sales)*100 as "Percentage of sales above 1 SOL",
(n_sales_above_10/all_sales)*100 as "Percentage of sales above 10 SOL"
from table1, table2
"""

sql3 = f"""
--Show the distribution of all Solana NFT sales on Solana. 
--What percentage of all sales have been above 1 SOL? Above 10 sol?
--How many unique wallets have made a NFT purchase that was above 10 SOL? Above 100 SOL?
WITH
  table1 as (
  SELECT
  count(distinct purchaser) as total_purchasers
  from solana.fact_nft_sales
  ),
  table2 as (
SELECT
count(distinct purchaser) as n_purchasers_above_10
from solana.fact_nft_sales
  where sales_amount >10
),
  table3 as (
SELECT
count(distinct purchaser) as n_purchasers_above_100
from solana.fact_nft_sales
  where sales_amount >100
)
SELECT
total_purchasers as "Total Solana NFT purchasers",
n_purchasers_above_10 as "Purchasers buying above 10 SOL",
n_purchasers_above_100 as "Purchasers buying above 100 SOL",
(n_purchasers_above_10/total_purchasers)*100 as "Percentage of purchasers that bought above 10 SOL",
(n_purchasers_above_100/total_purchasers)*100 as "Percentage of purchasers that bought above 100 SOL"
from table1, table2, table3
"""


# In[8]:


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


# In[16]:


import plotly.graph_objects as go
fig1 = go.Figure([go.Bar(x=df['price range'], y=df['number of sales'],marker_color=px.colors.qualitative.Plotly)])
fig1.update_layout(
    title='Distribution of sales by NFT price range',
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

fig2 = go.Figure([go.Bar(x=df['price range'], y=df['number of purchasers'],marker_color=px.colors.qualitative.Vivid)])
fig2.update_layout(
    title='Distribution of purchasers by NFT price range',
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
st.plotly_chart(fig2, theme="streamlit", use_container_width=True)


# In[38]:


fig3 = go.Figure([go.Scatter(x=df['number of purchasers'], y=df['number of sales'],marker_color=px.colors.qualitative.Plotly)])
fig3.update_layout(
    title='Number of sales vs number of purchasers',
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


# In[17]:


st.write('')


# In[44]:


import math

millnames = ['',' k',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


# In[43]:


st.markdown(""" <style> div.css-12w0qpk.e1tzin5v2{
 background-color: #f5f5f5;
 border: 2px solid;
 padding: 10px 5px 5px 5px;
 border-radius: 10px;
 color: #ffc300;
 box-shadow: 10px;
}
div.css-1r6slb0.e1tzin5v2{
 background-color: #f5f5f5;
 border: 2px solid; /* #900c3f */
 border-radius: 10px;
 padding: 10px 5px 5px 5px;
 color: green;
}
div.css-50ug3q.e16fv1kl3{
 font-weight: 900;
} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> div.css-ocqkz7.e1tzin5v4{
 background-color: #f5f5f5;
 border: 2px solid;
 padding: 10px 5px 5px 5px;
 border-radius: 10px;
 color: #ffc300;
 box-shadow: 10px;
}
div.css-keje6w.ce1tzin5v2{
 background-color: #f5f5f5;
 border: 2px solid; /* #900c3f */
 border-radius: 10px;
 padding: 10px 5px 5px 5px;
 color: orange;
}
div.css-12ukr4l.e1tzin5v0{
 font-weight: 900;
} 
</style> """, unsafe_allow_html=True)

col1,col2,col3 =st.columns(3)
with col1:
    st.metric('Number of NFT sales', millify(df2['total solana nft sales'][0]))
col2.metric('Number of sales above 1 SOL', millify(df2['sales above 1 sol'][0]))
col3.metric('Number of sales above 10 SOL', millify(df2['sales above 10 sol'][0]))

col4,col5=st.columns(2)
with col4:
    st.metric('Percentage of sales above 1 SOL',df2['percentage of sales above 1 sol'][0])
col5.metric('Percentage of sales above 10 SOL',df2['percentage of sales above 10 sol'][0])


# In[22]:


col1,col2,col3 =st.columns(3)
with col1:
    st.metric('Number of NFT purchasers', millify(df3['total solana nft purchasers'][0]))
col2.metric('Purchasers buying above 10 SOL', millify(df3['purchasers buying above 10 sol'][0]))
col3.metric('Purchasers buying above 100 SOL', millify(df3['purchasers buying above 100 sol'][0]))

col4,col5=st.columns(2)
with col4:
    st.metric('% of purchasers buying above 10 SOL',df3['percentage of purchasers that bought above 10 sol'][0])
col5.metric('% of purchasers buying above 100 SOL',df3['percentage of purchasers that bought above 100 sol'][0])


# In[25]:


sql4 = f"""
WITH
  solana_sales as (
SELECT
trunc(block_timestamp,'day') as date,
  max(sales_amount) as high_NFT_price_sale
from solana.fact_nft_sales 
group by 1
order by 1 asc
  )
SELECT
x.date,
x.high_NFT_price_sale as "High Solana NFT price sale",
lag(x.high_NFT_price_sale,1) over (order by x.date) as lasts,
((x.high_NFT_price_sale-lasts)/lasts)*100 as "High Solana NFT price sale % growth"
from solana_sales x
  where x.date>='2022-01-01'
order by 1 asc
"""

sql5="""
--Show the distribution of all Solana NFT sales on Solana. 
--What percentage of all sales have been above 1 SOL? Above 10 sol?
--How many unique wallets have made a NFT purchase that was above 10 SOL? Above 100 SOL?
WITH
  solana_sales as (
SELECT
trunc(block_timestamp,'day') as date,
  max(sales_amount) as high_NFT_price_sale
from solana.fact_nft_sales where date>='2022-01-01'
group by 1
order by 1 asc
  ),
  final_data as (
SELECT
x.date,
x.high_NFT_price_sale as "High Solana NFT price sale",
lag(x.high_NFT_price_sale,1) over (order by x.date) as lasts,
((x.high_NFT_price_sale-lasts)/lasts)*100 as "High Solana NFT price sale % growth"
from solana_sales x
  where x.date >='2022-01-01'
order by 1 asc
  )
SELECT
date,
  "High Solana NFT price sale % growth" as "NFT price sale growth",
  sum("NFT price sale growth") over (order by date) as "Cumulative growth"
from final_data 
order by 1 asc
"""


# In[26]:


results4 = compute(sql4)
df4 = pd.DataFrame(results4.records)
df4.info()

results5 = compute(sql5)
df5 = pd.DataFrame(results5.records)
df5.info()


# In[36]:


fig1 = px.line(df4, x="date", y="high solana nft price sale", color_discrete_sequence=px.colors.qualitative.Plotly)
fig1.update_layout(
    title='Highest Solana NFT price sale evolution',
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
st.write('')


# In[40]:


import altair as alt
base=alt.Chart(df5).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
line=base.mark_line(color='darkgreen').encode(y=alt.Y('nft price sale growth:Q', axis=alt.Axis(grid=True)))
bar=base.mark_bar(color='green',opacity=0.5).encode(y='cumulative growth:Q')

st.altair_chart((line + bar).resolve_scale(y='independent').properties(title='Daily and cumulative highest sale price % growth',width=600))


# In[ ]:





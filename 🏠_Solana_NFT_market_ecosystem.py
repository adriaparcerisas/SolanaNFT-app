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
import altair as alt
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[2]:


st.title('Solana NFT market ecosystem')


# In[8]:


st.markdown("**Solana** is a platform that seeks to provide a foundation for decentralized applications (dapps) in a way that prioritizes scalability. With this aim, Solana is one of several competing blockchain projects such as Ethereum, Zilliqa, or Cardano that hopes to grow an ecosystem of cryptocurrency-powered products and services.")
st.markdown("To differentiate itself, Solana introduces a combination of architectural design choices that attempts to offer faster transaction settlement times and an infrastructure that focuses on flexibility that enables developers to write and launch customizable applications in multiple programming languages [1](https://www.kraken.com/learn/what-is-solana-sol).")
st.write("")
st.markdown("One of the main characteristics of Solana network are the **_Non-Fungible Tokens (NFTs)_**. Last year, the market growth exponentially and consequently, the number of marketplaces related to NFT to be purchased increased as well.")
st.markdown("NFTs have been the trending topic of cryptowolrd over the past year. In fact, emblematic persons like _Mark Zuckenberg_ told about that and basically, put their enterprise name Facebook a different name so called _Meta_ in reference to Metaverse, the world of NFTs. Thanks to that, the growth of this type of tokens increased exponentially in all the blockchain networks. One of the main networks have been Solana and in this dashboard we are gonna analyze several metrics about their growth. ")
st.write("")
st.markdown("This dashboard represents a **Solana Secondary NFT Market** trends. It is intended to provide an overview of the current market for NFTs in **Solana**. The idea is that readers can have at their disposal a tool to see the current volume of NFT sales, which are the most popular secondary markets, as well as to see other metrics such as the number of users, the average price per sale of NFTs, etc. All the metrics are displayed in a daily, weekly and monthly basis in both, global and by each marketplace ways.")
st.markdown("Finally, a current metrics about each Solana NFT collection is displayed. The metrics corresponds to volume, popularity, sales, and percentage growth daily and weekly.")
            


# In[9]:


st.markdown("To display all the information properly and make the app more readable and user-friendly, it has been divided in several parts. You can find information about each different section by navigating on the sidebar pages.")


# In[12]:


st.markdown("These includes:") 
st.markdown("1. **_General NFT trends_**")
st.markdown("2. **_NFT sector growth_**")
st.markdown("3. **_Marketplaces competition_**")
st.markdown("4. **_NFT royalties_**")
st.markdown("5. **_NFT purchasing behavior_**")
st.markdown("6. **_Collection trends_**")

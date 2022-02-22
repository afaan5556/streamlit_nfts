import pandas as pd
import streamlit as st
import numpy as np
import altair as alt

"""
# Streamlit NFT data
##### _Combining two topics I know jack about_
They say the best way to learn something new is to just dive right in. Here I am combining my complete ignorance on the [Streamlit](https://streamlit.io/) open source project and the world of NFTs with the hope of learning something along the way.

By [Afaan Naqvi](https://www.linkedin.com/in/afaan-naqvi-30767bb/)
"""

"""
### Dataset
This project uses the [NFT Collections](https://www.kaggle.com/hemil26/nft-collections-dataset) dataset available on [Kaggle](https://kaggle.com) which consists of 250 collections and their all time statistics such as sales, transactions, ownership and buyers.
"""

# Read data
nft_df = pd.read_csv("nft_sales.csv")
# Show data
nft_df

# Prep data: Convert strings to int
nft_df["Sales"] = nft_df["Sales"].apply(lambda x: x[1:] if x[0] == '$' else x)

for i in ["Sales", "Buyers", "Txns", "Owners"]:
    nft_df[i] = nft_df[i].apply(lambda x: x.replace(",", "") if isinstance(x, str) else x)
    nft_df[i] = nft_df[i].apply(lambda x: np.nan_to_num(x))
    nft_df[i] = nft_df[i].astype(int)

"""
### Basic charts and filters
A couple of slider filter controlled charts of that data? Streamlit can do it with a few lines of code!
"""

min_buyers = int(nft_df["Buyers"].min())
min_owners = int(nft_df["Owners"].min())
max_buyers = int(nft_df["Buyers"].max())
max_owners = int(nft_df["Owners"].max())

# min_buyers = st.slider("Minimum numer of buyers", min_buyers, max_buyers, (min_buyers, max_buyers))
buyers_slider = st.slider("Number of Buyers", value=[min_buyers, max_buyers])
# min_owners = st.slider("Minimum number of owners", min_owners, max_owners, (min_owners, max_owners))
owners_slider = st.slider("Number of Owners", value=[min_owners, max_owners])


nft_df_filtered = nft_df[(nft_df["Buyers"] >= buyers_slider[0]) & (nft_df["Owners"] >= owners_slider[0]) & (nft_df["Buyers"] <= buyers_slider[1]) & (nft_df["Owners"] <= owners_slider[1])]
# nft_df_filtered = nft_df[(nft_df["Buyers"] >= min_buyers) & (nft_df["Owners"] >= min_owners)]

# filtered_collections = nft_df_filtered.shape[0]
filtered_sales = nft_df_filtered["Sales"].sum()
filtered_collections = (f"{nft_df_filtered.shape[0]:,}")
filtered_sales = (f"{nft_df_filtered['Sales'].sum():,}")

filtered_highlight = """
##### *Total Sales:* ${}
##### *Number of Collections:* {}
""".format(filtered_sales, filtered_collections)

filtered_highlight

nft_df_filtered_plot = alt.Chart(nft_df_filtered).mark_circle().encode(
     x='Owners', y='Buyers', size='Sales', color='Txns', tooltip=['Collections', 'Owners', 'Buyers', 'Sales', 'Txns'])

st.altair_chart(nft_df_filtered_plot, use_container_width=True)


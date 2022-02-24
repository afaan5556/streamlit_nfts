import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
from PIL import Image

bored_ape_image = Image.open('images/bored_ape.png')

"""
# Streamlit and NFTs
##### _Combining two topics I know jack about_
They say the best way to learn something new is to just dive right in. Here I am combining my complete ignorance on the [Streamlit](https://streamlit.io/) open source project and the world of NFTs with the hope of learning something along the way.

By [Afaan Naqvi](https://www.linkedin.com/in/afaan-naqvi-30767bb/)
"""

"""
### What is an NFT?
This is an NFT.
"""
st.image(bored_ape_image, caption='The NFT for this Bored Ape Yach Club image is worth $92,000!!')
"""
Specifically, this is a digitally saved copy of an original digital image, the associated NFT for which is NFT 8520 from the [Bored Ape Yacht Club](https://boredapeyachtclub.com/#/) collection, which (at the time of writing) had a total sales volume of $783,882,186.
##### EXACTLY!

What the heck is going on in this world? Well, the phenomenon of completely irrational and overpriced valuations we know and can not explain in the physical art world has entered the digital world with a bang!

If that sales volume (for this single collection of NFTs) isn't mind boggling enough, consider how many buyers, owners, and transactions are involved:
- Buyers: 8,284
- Owners: 5,862
- Transactions: 22,584
"""


"""
### Dataset
Ok, so with that out of the way, here is what I did for this weekend dive into the world of NFTs using Streamlit.
I grabbed this [NFT Collections](https://www.kaggle.com/hemil26/nft-collections-dataset) dataset available on [Kaggle](https://kaggle.com) which consists of 250 collections and their all time statistics such as sales, transactions, ownership and buyers.
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
While completely made up and over-priced valuations are not my jam, Streamlit absolutely is. How about a scatter plot of the above data controlled by a couple of slider filters?
Streamlit can do that with just the following lines of code!
"""

min_buyers = int(nft_df["Buyers"].min())
min_owners = int(nft_df["Owners"].min())
max_buyers = int(nft_df["Buyers"].max())
max_owners = int(nft_df["Owners"].max())

sliders_code = '''buyers_slider = st.slider("Number of Buyers", value=[min_buyers, max_buyers])
owners_slider = st.slider("Number of Owners", value=[min_owners, max_owners])

nft_df_filtered = nft_df[(nft_df["Buyers"] >= buyers_slider[0]) & (nft_df["Owners"] >= owners_slider[0]) & (nft_df["Buyers"] <= buyers_slider[1]) & (nft_df["Owners"] <= owners_slider[1])]
nft_df_filtered_plot = alt.Chart(nft_df_filtered).mark_circle().encode(
     x='Owners', y='Buyers', size='Sales', color='Txns', tooltip=['Collections', 'Owners', 'Buyers', 'Sales', 'Txns'])

st.altair_chart(nft_df_filtered_plot, use_container_width=True)
'''

st.code(sliders_code, language='python')

buyers_slider = st.slider("Number of Buyers", value=[min_buyers, max_buyers])
owners_slider = st.slider("Number of Owners", value=[min_owners, max_owners])

nft_df_filtered = nft_df[(nft_df["Buyers"] >= buyers_slider[0]) & (nft_df["Owners"] >= owners_slider[0]) & (nft_df["Buyers"] <= buyers_slider[1]) & (nft_df["Owners"] <= owners_slider[1])]

filtered_sales = nft_df_filtered["Sales"].sum()
filtered_collections = (f"{nft_df_filtered.shape[0]:,}")
filtered_sales = (f"{nft_df_filtered['Sales'].sum():,}")


nft_df_filtered_plot = alt.Chart(nft_df_filtered).mark_circle().encode(
     x='Owners', y='Buyers', size='Sales', color='Txns', tooltip=['Collections', 'Owners', 'Buyers', 'Sales', 'Txns'])

st.altair_chart(nft_df_filtered_plot, use_container_width=True)

filtered_highlight = """
###### *Total Sales:* ${}
###### *Total Collections:* {}
""".format(filtered_sales, filtered_collections)

filtered_highlight

"""
##### HOW COOL IS THAT?
You might have also noticed from the above code snippet that Streamlit requires writing code only in Python (well, ok, also Markdown) which, if you are a perennial Javascript scardy-cat like me, is like Christmas coming early!
"""

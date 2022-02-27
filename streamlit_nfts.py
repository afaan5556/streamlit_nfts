import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
from PIL import Image
import plotly.express as px

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
st.image(bored_ape_image, caption='The NFT for this Bored Ape Yacht Club image is worth $92,000!!')
"""
Specifically, this is a digitally saved copy of an original digital image, the associated NFT for which is NFT 8520 worth around **$92,000.**
###### EXACTLY!

What the heck is going on in this world?  Well, the phenomenon of completely irrational and overpriced valuations we know and can not explain in the physical art world has entered the digital world with a bang!

If that wasn't enough of a sticker shock, consider that this digital artwork is part of the [Bored Ape Yacht Club](https://boredapeyachtclub.com/#/) collection, which (at the time of writing) had a total sales volume of $783,882,186.
If that sales volume (for this single collection of NFTs) isn't mind boggling enough, consider how many buyers, owners, and transactions are involved:
- Buyers: 8,284
- Owners: 5,862
- Transactions: 22,584
"""


"""
### Dataset
Ok, so with that silliness out of the way, here is what I did for this weekend dive into the world of NFTs using Streamlit.
I grabbed this [NFT Collections](https://www.kaggle.com/hemil26/nft-collections-dataset) dataset available on [Kaggle](https://kaggle.com) which consists of 250 collections and their all time statistics such as sales, transactions, ownership and buyers.

It looks something like this.
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
### Streamlit is lit
While completely made up and over-priced valuations are not my jam, Streamlit absolutely is. How about a scatter plot of the above data controlled by a couple of slider filters?
Streamlit can do that with just the following lines of code!
"""

min_buyers = int(nft_df["Buyers"].min())
min_owners = int(nft_df["Owners"].min())
max_buyers = int(nft_df["Buyers"].max())
max_owners = int(nft_df["Owners"].max())

scatter_sliders_code = '''buyers_slider = st.slider("Number of Buyers", value=[min_buyers, max_buyers])
owners_slider = st.slider("Number of Owners", value=[min_owners, max_owners])

nft_df_filtered_scatter = nft_df[(nft_df["Buyers"] >= buyers_slider[0]) & (nft_df["Owners"] >= owners_slider[0]) & (nft_df["Buyers"] <= buyers_slider[1]) & (nft_df["Owners"] <= owners_slider[1])]
nft_df_filtered_scatter_plot = alt.Chart(nft_df_filtered_scatter).mark_circle().encode(
     x='Owners', y='Buyers', size='Sales', color='Txns', tooltip=['Collections', 'Owners', 'Buyers', 'Sales', 'Txns'])

st.altair_chart(nft_df_filtered_scatter_plot, use_container_width=True)
'''

st.code(scatter_sliders_code, language='python')

buyers_slider = st.slider("Number of Buyers", value=[min_buyers, max_buyers])
owners_slider = st.slider("Number of Owners", value=[min_owners, max_owners])

nft_df_filtered_scatter = nft_df[(nft_df["Buyers"] >= buyers_slider[0]) & (nft_df["Owners"] >= owners_slider[0]) & (nft_df["Buyers"] <= buyers_slider[1]) & (nft_df["Owners"] <= owners_slider[1])]

scatter_filtered_sales = nft_df_filtered_scatter["Sales"].sum()
scatter_filtered_collections = (f"{nft_df_filtered_scatter.shape[0]:,}")
scatter_filtered_sales = (f"{nft_df_filtered_scatter['Sales'].sum():,}")


nft_df_filtered_scatter_plot = alt.Chart(nft_df_filtered_scatter).mark_circle().encode(
     x='Owners', y='Buyers', size='Sales', color='Txns', tooltip=['Collections', 'Owners', 'Buyers', 'Sales', 'Txns'])

st.altair_chart(nft_df_filtered_scatter_plot, use_container_width=True)

filtered_highlight_collections = """
### {}
*Filtered Collections* 
""".format(scatter_filtered_collections)

filtered_highlight_sales = """
### ${}
*Filtered Sales* 
""".format(scatter_filtered_sales)


scatter_col_1, scatter_col_2, scatter_col_3 = st.columns(3)
scatter_col_2.write(filtered_highlight_collections)
scatter_col_3.write(filtered_highlight_sales)
# filtered_highlight

"""
###### HOW COOL IS THAT?
You might have also noticed from the above code snippet that Streamlit requires writing code only in Python (well, ok, also Markdown) which, if you are a perennial Javascript scardy-cat like me, is like Christmas coming early!
"""

"""
### One more viz
How about a 2 X 2 tiled set of histograms, binning the counts of collections by each dimension, and controllable by double-ended sliders in the previous section?


Here is the code...


*Note that the data was trimmed here to the "interesting" portion of owners and buyers <= 10,000*
"""

hist_code = '''nft_df_filtered_hist = nft_df[(nft_df["Buyers"] >= buyers_slider[0]) & (nft_df["Owners"] >= owners_slider[0]) & (nft_df["Buyers"] <= buyers_slider[1]) & (nft_df["Owners"] <= owners_slider[1])]
# Remove outliers that are killing histograms
nft_df_filtered_hist = nft_df_filtered_hist[nft_df_filtered_hist["Owners"] <= 10000]
nft_df_filtered_hist = nft_df_filtered_hist[nft_df_filtered_hist["Buyers"] <= 10000]
# Build histograms
hist_buyers = px.histogram(nft_df_filtered_hist["Buyers"], x="Buyers")
hist_sales = px.histogram(nft_df_filtered_hist["Sales"], x="Sales")
hist_transactions = px.histogram(nft_df_filtered_hist["Txns"], x="Txns")
hist_owners = px.histogram(nft_df_filtered_hist["Owners"], x="Owners")

# Set up 2X2 tiles
hist_col_1, hist_col_2 = st.columns(2)
hist_col_3, hist_col_4 = st.columns(2)

with hist_col_1:
     st.write("Sales")
     st.plotly_chart(hist_sales, use_container_width=True)

with hist_col_2:
     st.write("Buyers")
     st.plotly_chart(hist_buyers, use_container_width=True)

with hist_col_3:
     st.write("Transactions")
     st.plotly_chart(hist_transactions, use_container_width=True)

with hist_col_4:
     st.write("Owners")
     st.plotly_chart(hist_owners, use_container_width=True)
'''

st.code(hist_code, language='python')

nft_df_filtered_hist = nft_df[(nft_df["Buyers"] >= buyers_slider[0]) & (nft_df["Owners"] >= owners_slider[0]) & (nft_df["Buyers"] <= buyers_slider[1]) & (nft_df["Owners"] <= owners_slider[1])]
# Remove outliers that are killing histograms
nft_df_filtered_hist = nft_df_filtered_hist[nft_df_filtered_hist["Owners"] <= 10000]
nft_df_filtered_hist = nft_df_filtered_hist[nft_df_filtered_hist["Buyers"] <= 10000]


"""
... and bang, here is the result:

"""

# Build histograms
hist_buyers = px.histogram(nft_df_filtered_hist["Buyers"], x="Buyers")
hist_sales = px.histogram(nft_df_filtered_hist["Sales"], x="Sales")
hist_transactions = px.histogram(nft_df_filtered_hist["Txns"], x="Txns")
hist_owners = px.histogram(nft_df_filtered_hist["Owners"], x="Owners")

# Set up 2X2 tiles
hist_col_1, hist_col_2 = st.columns(2)
hist_col_3, hist_col_4 = st.columns(2)

with hist_col_1:
     st.write("Sales")
     st.plotly_chart(hist_sales, use_container_width=True)

with hist_col_2:
     st.write("Buyers")
     st.plotly_chart(hist_buyers, use_container_width=True)

with hist_col_3:
     st.write("Transactions")
     st.plotly_chart(hist_transactions, use_container_width=True)

with hist_col_4:
     st.write("Owners")
     st.plotly_chart(hist_owners, use_container_width=True)

"""
### Conclusion
Streamlit is fantastic! It blew my mind like the first time I used Jupyter Notebook, except the end result ends up deployed on the web instead of you your local-host. Definitely a rabbit hole that I expect to find myself deep in during the coming weeks!!

As for NFT's, well, I wouldn't pay more than a few bucks for THE Mona Lisa or THE Starry Night, so I do not expect to be getting on the wagon with their 2020's digital cousins.

# Thanks for reading!
"""
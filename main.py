from bz2 import compress
import gzip
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# import plotly.express as px
import plotly.express as px 
import mplcursors
import numpy as np
from datetime import datetime




df = pd.read_csv("data_source/cleaned_data2.csv",compression="gzip")

# df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
# df['date'] = df['date'].dt.date
# new_row = {'supermarket': 'all', 'unit': 'all', 'names': 'all','date':'all', 'category': 'all'}
# df = df.append(new_row, ignore_index=True)
# df.loc[len(df)+1]=new_row
filtered_df = df 

default_value = "all"

Store = df['supermarket'].drop_duplicates()
# selectStore = st.sidebar.multiselect("Select Store : ", df['supermarket'].drop_duplicates(), index=len(Store)-1,multiple=True)
all_store =df['supermarket'].unique()
selectStore = st.sidebar.multiselect("Select Store:", all_store, default=all_store)
filtered_df =df[df['supermarket'].isin(selectStore)]   

searchItem = st.sidebar.text_input("Search by item name : ")
if not searchItem : 
    filtered_df = filtered_df

else:
    filtered_df = df[df['names'].str.contains(searchItem, na=False, case=False)]


selectDate = st.sidebar.multiselect("Select date:", df['date'].drop_duplicates())
filtered_df =df[df['date'].isin(selectDate)]   

all_categories = df['category'].unique()
selectCat = st.sidebar.multiselect("Select Category:", all_categories, default=all_categories)
filtered_df =df[df['category'].isin(selectCat)]   


st.dataframe(filtered_df)


Cat = df['category'].value_counts()


tab1,tab2 = st.tabs(["category", "store"])

with tab1 : 
    Cat = filtered_df['category'].value_counts()
    fig = px.pie(names=Cat.index, values=Cat.values, title='Category Counts',
             hover_data={'category': Cat.index})
    st.plotly_chart(fig)
with tab2 : 
    store = filtered_df['supermarket'].value_counts()
    fig = px.pie(names=store.index, values=store.values, title='Store Counts',
             hover_data={'category': store.index})
    st.plotly_chart(fig)


tab3, tab4 = st.tabs(["prices","prices by unit"])

with tab3 : 
    fig, ax = plt.subplots()
    total_price_by_date = filtered_df.groupby('date')['prices_(¬£)'].sum().reset_index()
    fig = px.line(total_price_by_date, x='date', y='prices_(¬£)')

    st.plotly_chart(fig)
with tab4 : 
    fig, ax = plt.subplots()
    total_unit_price_by_date = filtered_df.groupby('date')['prices_unit_(¬£)'].sum().reset_index()
    fig = px.line(total_unit_price_by_date, x='date', y='prices_unit_(¬£)')
    # df['category']
    st.plotly_chart(fig)



tab5,tab6 =st.tabs(["Price Percentage Compared from first data","Price per unit Percentage Compared from first data" ])

with tab5:
    fig, ax = plt.subplots()
    min_date = filtered_df["date"].min()
    max_date = filtered_df["date"].max()

    early_price=filtered_df[filtered_df['date'] == min_date]['prices_(¬£)'].values.sum()
    late_price=filtered_df[filtered_df['date'] == max_date]['prices_(¬£)'].values.sum()

    price_change=((late_price-early_price)/early_price*100)

    st.markdown(f"The percentage increase is: {price_change:.2f}%")

with tab6:
    fig, ax = plt.subplots()
    min_date = filtered_df["date"].min()
    max_date = filtered_df["date"].max()

    early_price=filtered_df[filtered_df['date'] == min_date]['prices_unit_(¬£)'].values.sum()
    late_price=filtered_df[filtered_df['date'] == max_date]['prices_unit_(¬£)'].values.sum()

    price_change=((late_price-early_price)/early_price*100)

    st.markdown(f"The percentage increase is: {price_change:.2f}%")



tab7,tab8 =st.tabs(["Price Percentage Compared from previous data","Price per unit Percentage Compared from previous data" ])

with tab7:
    fig, ax = plt.subplots()
    date_df=filtered_df['date'].unique()
    # date_df = np.array([datetime.strptime(date_str, '%Y-%m-%d') for date_str in date_df])

    date_df.sort()
    idx= len(date_df)-2
    prev_date= date_df[idx]
    prev_date_main= filtered_df[filtered_df["date"] == prev_date]
    max_date = df["date"].max()

    
    early_price=filtered_df[filtered_df['date'] == prev_date]['prices_(¬£)'].values.sum()
    late_price=filtered_df[filtered_df['date'] == max_date]['prices_(¬£)'].values.sum()

    price_change=((late_price-early_price)/early_price*100)

    st.markdown(f"The percentage increase is: {price_change:.2f}%")

with tab8:
    fig, ax = plt.subplots()
    date_df=filtered_df['date'].unique()
    # date_df = np.array([datetime.strptime(date_str, '%Y-%m-%d') for date_str in date_df])

    date_df.sort()
    idx= len(date_df)-2
    prev_date= date_df[idx]
    prev_date_main= filtered_df[filtered_df["date"] == prev_date]
    max_date = df["date"].max()
    
    
    early_price=filtered_df[filtered_df['date'] == prev_date]['prices_unit_(¬£)'].values.sum()
    late_price=filtered_df[filtered_df['date'] == max_date]['prices_unit_(¬£)'].values.sum()

    price_change=((late_price-early_price)/early_price*100)

    st.markdown(f"The percentage increase is: {price_change:.2f}%")


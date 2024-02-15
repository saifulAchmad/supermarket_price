import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# import plotly.express as px
import plotly.express as px 
import mplcursors



df = pd.read_csv("data_source/cleaned_data2.csv")

# df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
# df['date'] = df['date'].dt.date
# new_row = {'supermarket': 'all', 'unit': 'all', 'names': 'all','date':'all', 'category': 'all'}
# df = df.append(new_row, ignore_index=True)
# df.loc[len(df)+1]=new_row
filtered_df = df 

default_value = "all"

Store = df['supermarket'].drop_duplicates()
# selectStore = st.sidebar.multiselect("Select Store : ", df['supermarket'].drop_duplicates(), index=len(Store)-1,multiple=True)
selectStore = st.sidebar.multiselect("Select Store:", df['supermarket'].drop_duplicates())
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

fig, ax = plt.subplots()
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
    total_price_by_date = df.groupby('date')['prices_(¬£)'].sum().reset_index()
    fig = px.line(total_price_by_date, x='date', y='prices_(¬£)')

    st.plotly_chart(fig)
with tab4 : 
    total_unit_price_by_date = df.groupby('date')['prices_unit_(¬£)'].sum().reset_index()
    fig = px.line(total_unit_price_by_date, x='date', y='prices_unit_(¬£)')
    df['category']
    st.plotly_chart(fig)

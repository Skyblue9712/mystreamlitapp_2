import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# configure the page
st.set_page_config(
    page_title='Data Science App',
    page_icon='🎈',
    layout='centered'

)
# load the data
@st.cache_data()
def load_data():
   url='data/Top_rated_movies1.csv'
   df=pd.read_csv(url,parse_dates=['release_date'])
   return df
#built the ui
st.title("Data Science App")
with st.spinner("Loading data...."):
     df= load_data()
st.header("IMDB 8000movies dataset")
st.info("Raw Data in dataframe")
st.dataframe(df,use_container_width=True)


st.success("column information of the datasheet")
cols=df.columns.tolist()
st.subheader(f'Total columns {len(cols)} ➡ {"," .join(cols)}')
# add some graph and widget
st.header('basic data visualization')
gop=['bar','line','area']
c1,c2=st.columns(2)
sel_op=c1.selectbox("select the type of plot by popularity",gop)
subset=df.sort_values(by='popularity')[:50]

if sel_op==gop[0]:
    fig=px.bar(subset,x='title',y='popularity',log_y=True)
elif sel_op==gop[1]:
    fig=px.line(subset,x='title',y='popularity',log_y=True)
elif sel_op==gop[2]:
    fig=px.area(subset,x='title',y='popularity',log_y=True)
c1.plotly_chart(fig, use_container_width=True)  

sel_op2=c2.selectbox("select the type of plot by vote_count",gop)
subset2=df.sort_values(by='vote_count')[:50]
if sel_op2==gop[0]:
    fig=px.bar(subset2,x='title',y='vote_count',log_y=True)
elif sel_op2==gop[1]:
    fig=px.line(subset2,x='title',y='vote_count',log_y=True)
elif sel_op2==gop[2]:
    fig=px.area(subset2,x='title',y='vote_count',log_y=True)
c2.plotly_chart(fig, use_container_width=True)
# adjust layout
t1,t2,t3=st.tabs(['bivariate','trivariate','about'])
nums_cols=df.select_dtypes(include=np.number).columns.tolist()
with t1:
    c1,c2=st.columns(2)
    col1=c1.radio('select the first column for scatter plot',nums_cols)
    col2=c2.radio('select the second column for scatter plot',nums_cols)
    fig = px.scatter(df,x=col1,y=col2,title=f'{col1} vs {col2}')
    st.plotly_chart(fig,use_container_width=True)

with t2:
    c1,c2,c3=st.columns(3)
    col1=c1.radio('select the first column for scatter plot for 3d',nums_cols)
    col2=c2.radio('select the second column for scatter plot for 3d',nums_cols)
    col3=c3.radio('select the third column for scatter plot for 3d',nums_cols)
    fig = px.scatter_3d(df,x=col1,y=col2,z=col3,title=f'{col1} vs {col2} vs {col3}',height=700)
    st.plotly_chart(fig,use_container_width=True)

# how to run the app
# open terminal and run:
#streamlit run main.py
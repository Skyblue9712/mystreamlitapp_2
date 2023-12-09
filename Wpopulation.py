import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# configure the page
st.set_page_config(
    page_title='World Pouplation 2023',
    page_icon='🌎',
    layout='wide'

)
def colored_text(text, color):
    return f'<span style="color:{color};font-size:20px">{text}</span>'

heading_color=''
# load the data
@st.cache_data()
def load_data():
   url=r'data\2023_population.csv'
   df=pd.read_csv(url)
   return df
#built the ui
st.title(":bar_chart: 2023 Population Analysis")
st.markdown('<style>div.block-container{padding-top:2.5rem;}</style>',unsafe_allow_html=True)
with st.spinner("Loading data...."):
     df= load_data()
st.subheader(":point_right: 2023 World Population dataset")
st.info("Raw Data in dataframe")
i=[]

df['2023_last_updated'] = pd.to_numeric(df['2023_last_updated'].str.replace(',', '') , errors='coerce')
df['2022_population'] = pd.to_numeric(df['2022_population'].str.replace(',', '') , errors='coerce')
df['world_%'] = pd.to_numeric(df['world_%'].str.replace('%', '') , errors='coerce')
df=df[~df['2023_last_updated'].isnull()]
df=df[~df['world_%'].isnull()]

def convert_K_M_to_numeric(value):
    if 'K' in value:
        return float(value.replace('K', ''))*1000
    elif 'M' in value:
        return float(value.replace('M', ''))*1000000
    elif '<' in value:
        return float(value.replace('<',''))
    elif ',' in value:
        return float(value.replace(',',''))
    elif '%' in value:
        return float(value.replace('%',''))
    else:
        return float(value)


df['land_area_sq_km'] = df['land_area_sq_km'].apply(convert_K_M_to_numeric)
df['area_sq_km'] = df['area_sq_km'].apply(convert_K_M_to_numeric)
df['growth_rate'] = df['growth_rate'].apply(convert_K_M_to_numeric)
df['density_/sq_km'] = df['density_/sq_km'].apply(convert_K_M_to_numeric)

df=df.rename(columns={"iso_code":"code",'2023_last_updated':'2023_populaton'})
df.drop(['un_member','rank'],axis=1,inplace=True)
df.sort_values(by='2023_populaton',ascending=False,inplace=True)
for k in range(1,df.shape[0]+1,1): i.append(k)
df.index=i

st.dataframe(df,use_container_width=True)


st.success("column information of the datasheet")
cols=df.columns.tolist()
heading_color='blue'
st.markdown(colored_text(f'Total columns {len(cols)} ➡ {"," .join(cols)}', heading_color), unsafe_allow_html=True)

# add some graph and widget
st.header('basic data visualization')
gop=['bar','line','area']
c1,c2=st.columns(2)
c1.info('Top 50 populated country',icon='🌐')
sel_op=c1.selectbox("select the type of plot for population density",gop)

subset=df[:21]

if sel_op==gop[0]:
    fig=px.bar(subset,x='country',y='2023_populaton',log_y=True)
elif sel_op==gop[1]:
    fig=px.line(subset,x='country',y='2023_populaton',log_y=True)
elif sel_op==gop[2]:
    fig=px.area(subset,x='country',y='2023_populaton',log_y=True)


c1.plotly_chart(fig, use_container_width=True)  

c2.info('Last 50 populated country',icon='🌐')

sel_op2=c2.selectbox("select the type of plot by vote_count",gop)
subset2=df[-20:]
if sel_op2==gop[0]:
    fig=px.bar(subset2,x='country',y='2023_populaton',log_y=True)
elif sel_op2==gop[1]:
    fig=px.line(subset2,x='country',y='2023_populaton',log_y=True)
elif sel_op2==gop[2]:
    fig=px.area(subset2,x='country',y='2023_populaton',log_y=True)
c2.plotly_chart(fig, use_container_width=True)
# adjust layout
t1,t2,t3=st.tabs(['bivariate','trivariate','about'])
nums_cols=df.select_dtypes(include=['object',np.number]).columns.tolist()

with t1:
    c1,c2=st.columns(2)
    col1=c1.radio('select the first column for scatter plot',nums_cols)
    col2=c2.radio('select the second column for scatter plot',nums_cols)
    fig = px.scatter(df.head(20),x=col1,y=col2,title=f'{col1} vs {col2}')
    st.plotly_chart(fig,use_container_width=True)
    if pd.api.types.is_numeric_dtype(df[col1]):
        fig = px.pie(df.head(20), values=col1, names='country', title=f'Pie Chart 👉{ col1} ')
        c1.plotly_chart(fig,use_container_width=True)
    if pd.api.types.is_numeric_dtype(df[col2]):
        fig = px.pie(df.head(20), values=col2, names='country', title=f'Pie Chart 👉{ col2} ')
        c2.plotly_chart(fig,use_container_width=True)
   
    

with t2:
    c1,c2,c3=st.columns(3)
    col1=c1.radio('select the first column for scatter plot for 3d',nums_cols)
    col2=c2.radio('select the second column for scatter plot for 3d',nums_cols)
    col3=c3.radio('select the third column for scatter plot for 3d',nums_cols)
    fig = px.scatter_3d(df.head(20),x=col1,y=col2,z=col3,title=f'{col1} vs {col2} vs {col3}',height=700)
    st.plotly_chart(fig,use_container_width=True)
    if pd.api.types.is_numeric_dtype(df[col1]):
        fig = px.pie(df.head(20), values=col1, names='country', title=f'Pie Chart 👉{ col1} ')
        c1.plotly_chart(fig,use_container_width=True)
    if pd.api.types.is_numeric_dtype(df[col2]):
        fig = px.pie(df.head(20), values=col2, names='country', title=f'Pie Chart 👉{ col2} ')
        c2.plotly_chart(fig,use_container_width=True)
    if pd.api.types.is_numeric_dtype(df[col3]):
        fig = px.pie(df.head(20), values=col2, names='country', title=f'Pie Chart 👉{ col3} ')
        c3.plotly_chart(fig,use_container_width=True)
    
with t3:
    st.text('''gfbcghgfcghdhgvmvcfgcvmcghcgj gfbcghgfcghdhgvmvcfgcvmcghcgj  gfbcghgfcghdhgvmvcfgcvmcghcgj
    gfbcghgfcghdhgvmvcfgcvmcghcgj gfbcghgfcghdhgvmvcfgcvmcghcgj  gfbcghgfcghdhgvmvcfgcvmcghcgj
    gfbcghgfcghdhgvmvcfgcvmcghcgj gfbcghgfcghdhgvmvcfgcvmcghcgj  gfbcghgfcghdhgvmvcfgcvmcghcgj
    gfbcghgfcghdhgvmvcfgcvmcghcgj gfbcghgfcghdhgvmvcfgcvmcghcgj  gfbcghgfcghdhgvmvcfgcvmcghcgj
    gfbcghgfcghdhgvmvcfgcvmcghcgj gfbcghgfcghdhgvmvcfgcvmcghcgj  gfbcghgfcghdhgvmvcfgcvmcghcgj
    gfbcghgfcghdhgvmvcfgcvmcghcgj gfbcghgfcghdhgvmvcfgcvmcghcgj  gfbcghgfcghdhgvmvcfgcvmcghcgj''')


# how to run the app
# open terminal and run:
#streamlit run main.py
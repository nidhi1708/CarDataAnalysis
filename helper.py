import streamlit as st
from functools import cache
from pandas_profiling import ProfileReport
import sweetviz as sv

@st.experimental_memo
def data_graph(df , col):
    df = df.dropna(subset=[col]) 
    data_Graph = df[col].value_counts().reset_index().sort_values('index')
    data_Graph.rename(columns={'index': col, col: 'No of Models'}, inplace=True)
    return data_Graph

@st.experimental_memo
def clean_data(df):
    df = df.rename(columns={'Make': 'Company', 'Ex-Showroom_Price': 'Price'})
    df['City_Mileage']=df['City_Mileage'].apply(lambda x: str(x).replace('?' , '') if '?' in str(x) else str(x))
    df['City_Mileage']=df['City_Mileage'].apply(lambda x: str(x).replace(',' , '.') if ',' in str(x) else str(x))
    df['City_Mileage']=df['City_Mileage'].apply(lambda x: str(x).replace('km/litre' , '') if 'km/litre' in str(x) else str(x))
    df['City_Mileage']=df['City_Mileage'].apply(lambda x: str(x).replace('-12.7' , '') if '-12.7' in str(x) else str(x))
    df['City_Mileage']=df['City_Mileage'].apply(lambda x: str(x).replace('26032' , '26.03') if '26032' in str(x) else str(x))
    df['City_Mileage']=df['City_Mileage'].astype('float')
    df['Displacement']=df['Displacement'].apply(lambda x: str(x).replace('cc' , '') if 'cc' in str(x) else str(x))
    return df

@st.experimental_memo
def temp_df(df):

    df = df.fillna('')
    df = df.replace(' ', '')

    df['Price'] = df['Price'].apply(lambda x: str(x).replace('Rs.', '') if 'Rs.' in str(x) else str(x))
    df['Price'] = df['Price'].apply(lambda x: str(x).replace(',', '') if ',' in str(x) else str(x))
    df['Price'] = df['Price'].apply(lambda x: int(x))
    #df['Displacement'] = df['Displacement'].astype('str').str.replace('cc', '')
    return df


@st.experimental_memo
def comp_df(df):
    comp_df = df.dropna(subset=['Company']) #dropping all the columns which don't have a company
    comp_df = comp_df.fillna('')
    comp_df = comp_df.replace(' ', '')
    return comp_df

@st.experimental_memo
def top_cars(df , fuel_type):
    new_df = df.dropna(subset=['Company'])
    final_df = new_df[new_df['Fuel_Type'] == fuel_type]
    df['Price'] = df['Price'].str.split(' ').str.get(1).str.replace(',', '').astype('int')
    final_df_new = final_df[['Company', 'Model', 'Price', 'Fuel_Type']].sort_values(by=['Price'],
                        ascending=False).reset_index().drop(['index'], axis=1).head(10)

    return final_df_new

@st.experimental_memo
def get_comp_data(df , company):
    comp_df = df[df['Company'] == company]
    final_df_new = comp_df[['Company', 'Model', 'Price', 'Fuel_Type']].sort_values(by=['Price'],
                    ascending=False).reset_index().drop( ['index'], axis=1).head(10)
    return final_df_new

@st.experimental_memo
def sort_via_price(df , p1 , p2):
    df = df[df['Price'] >= p1]
    df = df[df['Price'] < p2]
    return df

@st.experimental_memo
def get_col_list(df , col):
    list_res = df[col].unique().tolist()
    list_res.sort()
    list_res.insert(0, '-')
    return list_res

@st.experimental_memo
def get_model_data(df , comp , model , price):
    temp = df[df['Company'] == comp]
    temp = temp[temp['Model'] == model]
    temp = temp[temp['Price'] == price]
    return temp

@st.experimental_singleton
def generate_pandas_profile_report(df):
    profile = ProfileReport(df)
    return profile  

@st.experimental_singleton
def generate_sweetviz_report(df):
    report = sv.analyze(df)
    return report
   
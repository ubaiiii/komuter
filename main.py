import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime

df1 = pd.read_excel('BC-PS-BC-Hari-Bekerja-10072023.xlsx', sheet_name="Table 1")
df2 = pd.read_excel('BC-PS-BC-Hari-Bekerja-10072023.xlsx', sheet_name="Table 2")


with st.form(key='my_form'):
    departure = st.selectbox("Depart from", options=df1["Nombor Tren"].unique(), index=0)
    destination = st.selectbox("Destination from", options=df1["Nombor Tren"].unique(), index=1)
    submit_button = st.form_submit_button(label='Submit')


def trip_schedule(df_x, table):
     # check destination route if nan, drop col
    list_station = [ departure, destination]
    train_schedule = df_x.loc[df_x['Nombor Tren'].isin(list_station)]
    if ( table == "Table 2") :
        another_id = 0
    else:
        another_id = 1

    idx = 0
    column_to_be_drop = []
    for y in train_schedule:
        try:
            datetime.strptime((train_schedule.iat[another_id,idx]), '%H:%M').time()
        except:
            column_to_be_drop.append(idx)
        
        idx = idx + 1
    train_schedule.drop(train_schedule.columns[column_to_be_drop], axis=1, inplace=True) 
    return train_schedule



# identifying datasources
x = 99
y = 99
table = None

for index, row in df1.iterrows():
    if row['Nombor Tren'] == departure:
        x = index    
    if row['Nombor Tren'] == destination:
        y = index

    if ( y > x ) :
        print ( "X : ", x ,"Y : ", y , " Read from Table 2") 
        df = df2
        table = "Table 2"
    else :
        print ( "X : ", x ,"Y : ", y , " Read from Table 1") 
        df = df1
        table = "Table 1"







train_schedule = trip_schedule(df, table)

st.dataframe(train_schedule)







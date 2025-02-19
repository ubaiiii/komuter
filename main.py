# Step 1: Download latest train schedule from KTM web
# Step 2: Convert pdf to excel https://smallpdf.com/pdf-to-excel
#

import pandas as pd
import streamlit as st
from datetime import datetime, time,  timedelta

kl_time = datetime.now().now() + timedelta(hours=8)
masa = kl_time.time().strftime("%I:%M %p")
time_depart = kl_time.time().replace(second=0, microsecond=0)

excel_file_source = 'BCPS_2024_Hari Bekerja 02122024.xlsx'

df1 = pd.read_excel(excel_file_source, sheet_name="Table 1", skiprows=2)
df2 = pd.read_excel(excel_file_source, sheet_name="Table 2", skiprows=2)

st.title('KTM Komuter Timetable')
st.header('Weekdays only')
st.subheader('Batu Caves - Pulau Sebang')

st.info('Updated on 19th February 2025', icon="ℹ️")



form = st.form("my_form")
c = st.container()
c.departure = form.selectbox("Depart from", 
                             options=df1["NOMBOR TREN"].unique(), 
                             index=0)
c.destination = form.selectbox("Destination from", 
                               options=df1["NOMBOR TREN"].unique(), 
                               index=1)

st.write('Current time is  :', time_depart)

c.current_time = st.checkbox('Tick this :blue[checkbox] to check for different time :sunglasses:')  # noqa: E501

if c.current_time:    
        time_depart = st.slider( 
            "Choose your departure time :",
            value=(time(12, 00) ) )
# else:
#         time_depart = datetime.strptime((masa), '%H:%M').time() 

form.form_submit_button("Submit")






#st.write("You're scheduled for:", time_depart)

# lookup schedule
def trip_schedule(df_x, table):
    
 #   st.write("Time > ", time_depart)

     # check destination route if nan, drop col
    list_station = [ c.departure, c.destination]
    train_schedule = df_x.loc[df_x['NOMBOR TREN'].isin(list_station)]
    if ( table == "Table 1") :
        another_id = 1
  #      st.write("Table 1 : ", another_id)
    else:
        another_id = 0
   #     st.write("Table 2 : ", another_id)

    idx = 0
    column_to_be_drop = []
    for y in train_schedule:
        try:
            if ( datetime.strptime((train_schedule.iat[another_id,idx]), '%H:%M').time() ) < time_depart:  # noqa: E501
                column_to_be_drop.append(idx)
            else:
                datetime.strptime((train_schedule.iat[another_id,idx]), '%H:%M').time()
                if another_id == 1:
                    if ( datetime.strptime((train_schedule.iat[0,idx]), '%H:%M').time() ) < time_depart:  # noqa: E501
                        column_to_be_drop.append(idx)
#                        st.write("Dopped some more data", train_schedule[0,idx])
        except:  # noqa: E722
            column_to_be_drop.append(idx)
        
        #idx = idx + 1
        idx += 1
    train_schedule.drop(train_schedule.columns[column_to_be_drop], axis=1, inplace=True)   # noqa: E501
    
    return train_schedule



# identifying datasources
x = 99
y = 99
table = None

for index, row in df1.iterrows():
    if row['NOMBOR TREN'] == c.departure:
        x = index    
    if row['NOMBOR TREN'] == c.destination:
        y = index

    if ( y > x ) :
        # print ( "X : ", x ,"Y : ", y , " Read from Table 2") 
        df = df1
        table = "Table 1"
    else :
        # print ( "X : ", x ,"Y : ", y , " Read from Table 1") 
        df = df2
        table = "Table 2"


train_schedule = trip_schedule(df, table)

## formatting dataframe
schedule_tranpose = train_schedule.T

schedule_tranpose.columns = [c.departure, c.destination]

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# st.write(len(schedule_tranpose))

if ( len(schedule_tranpose) > 0 ) :
    # st.dataframe(schedule_tranpose)
    # Display a static table
    st.table(schedule_tranpose)
else:
    txt_message = f'No more train from {c.departure}  towards  {c.destination}'
    st.error(txt_message)












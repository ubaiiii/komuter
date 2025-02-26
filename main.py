import pandas as pd
import streamlit as st
from datetime import datetime, time, timedelta

# Custom CSS for better UI
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSelectbox>div>div>div>div {
        background-color: #f0f2f6;
        border-radius: 8px;
    }
    .stSlider>div>div>div>div {
        background-color: #4CAF50;
    }
    .stCheckbox>div>label {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# Step 1: Download latest train schedule from KTM web
# Step 2: Convert pdf to excel https://smallpdf.com/pdf-to-excel

kl_time = datetime.now() + timedelta(hours=8)
masa = kl_time.time().strftime("%I:%M %p")
time_depart = kl_time.time().replace(second=0, microsecond=0)

excel_file_source = 'BCPS_2024_Hari Bekerja 02122024.xlsx'

df1 = pd.read_excel(excel_file_source, sheet_name="Table 1", skiprows=2)
df2 = pd.read_excel(excel_file_source, sheet_name="Table 2", skiprows=2)

st.title('🚆 KTM Komuter Timetable')
st.header('Weekdays only')
st.subheader('Batu Caves - Pulau Sebang')

st.info('Updated on 19th February 2025', icon="ℹ️")

# Form for user input
with st.form("timetable_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        departure = st.selectbox("Depart from", options=df1["NOMBOR TREN"].unique(), index=0)
    
    with col2:
        destination = st.selectbox("Destination", options=df1["NOMBOR TREN"].unique(), index=1)
    
    st.write(f'Current time is: **{time_depart.strftime("%I:%M %p")}**')
    
    use_custom_time = st.checkbox('Tick this checkbox to choose a different departure time', value=False)
    
    if use_custom_time:
        time_depart = st.slider("Choose your departure time:", value=time_depart, step=timedelta(minutes=15))
    
    submitted = st.form_submit_button("Get Schedule")

# Function to lookup schedule
def trip_schedule(df_x, table):
    list_station = [departure, destination]
    train_schedule = df_x.loc[df_x['NOMBOR TREN'].isin(list_station)]
    
    another_id = 1 if table == "Table 1" else 0
    
    column_to_be_drop = []
    for idx, col in enumerate(train_schedule.columns):
        try:
            col_time = datetime.strptime(train_schedule.iat[another_id, idx], '%H:%M').time()
            if col_time < time_depart:
                column_to_be_drop.append(idx)
            elif another_id == 1:
                if datetime.strptime(train_schedule.iat[0, idx], '%H:%M').time() < time_depart:
                    column_to_be_drop.append(idx)
        except:
            column_to_be_drop.append(idx)
    
    train_schedule = train_schedule.drop(train_schedule.columns[column_to_be_drop], axis=1)
    return train_schedule

# Identifying datasources
x = y = 99
table = None

for index, row in df1.iterrows():
    if row['NOMBOR TREN'] == departure:
        x = index    
    if row['NOMBOR TREN'] == destination:
        y = index

    if y > x:
        df = df1
        table = "Table 1"
    else:
        df = df2
        table = "Table 2"

if submitted:
    train_schedule = trip_schedule(df, table)
    schedule_transpose = train_schedule.T
    schedule_transpose.columns = [departure, destination]

    # CSS to inject contained in a string
    hide_table_row_index = """
        <style>
        thead tr th:first-child {display:none}
        tbody th {display:none}
        </style>
        """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    if len(schedule_transpose) > 0:
        st.table(schedule_transpose)
    else:
        st.error(f'No more trains from {departure} towards {destination}')
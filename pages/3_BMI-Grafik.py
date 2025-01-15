import streamlit as st
import pandas as pd
from utils.app_manager import AppManager
from functions.bmi_data_manager import load_bmi_df

app_manager = AppManager()
app_manager.login_page()

data_handler = app_manager.get_user_data_handler()
bmi_df = data_handler.load('bmi.csv', initial_value=pd.DataFrame())

st.title('BMI Verlauf')

if bmi_df.empty:
    st.info('Keine BMI Daten vorhanden. Berechnen Sie Ihren BMI auf der Startseite.')
    st.stop()

# Sort dataframe by timestamp
bmi_df['timestamp'] = pd.to_datetime(bmi_df['timestamp'], format='%d.%m.%Y %H:%M:%S')
bmi_df = bmi_df.sort_values('timestamp')

# Weight over time
st.line_chart(data=bmi_df.set_index('timestamp')['weight'], 
                use_container_width=True)
st.caption('Gewicht über Zeit (kg)')

# Height over time 
st.line_chart(data=bmi_df.set_index('timestamp')['height'],
                use_container_width=True)
st.caption('Größe über Zeit (m)')

# BMI over time
st.line_chart(data=bmi_df.set_index('timestamp')['bmi'],
                use_container_width=True)
st.caption('BMI über Zeit')




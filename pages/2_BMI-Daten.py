import streamlit as st
import pandas as pd
from utils.app_manager import AppManager

app_manager = AppManager()
app_manager.login_page()

data_handler = app_manager.get_user_data_handler()
bmi_df = data_handler.load('bmi.csv', initial_value=pd.DataFrame())

st.title('BMI Werte')

if bmi_df.empty:
    st.info('Keine BMI Daten vorhanden. Berechnen Sie Ihren BMI auf der Startseite.')
    st.stop()

# Sort dataframe by timestamp
bmi_df['timestamp'] = pd.to_datetime(bmi_df['timestamp'], format='%d.%m.%Y %H:%M:%S')
bmi_df = bmi_df.sort_values('timestamp', ascending=False)

# Display table
st.dataframe(bmi_df)

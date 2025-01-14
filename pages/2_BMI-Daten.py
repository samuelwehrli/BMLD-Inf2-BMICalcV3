import streamlit as st
import pandas as pd
from utils.app_manager import AppManager
from functions.bmi_data_manager import load_bmi_df

app_manager = AppManager()
app_manager.check_login()

bmi_file = app_manager.get_user_data_file('bmi.csv')
bmi_df = load_bmi_df(bmi_file)

st.title('BMI Werte')

if bmi_df.empty:
    st.info('Keine BMI Daten vorhanden. Berechnen Sie Ihren BMI auf der Startseite.')
    st.stop()

# Sort dataframe by timestamp
bmi_df['timestamp'] = pd.to_datetime(bmi_df['timestamp'], format='%d.%m.%Y %H:%M:%S')
bmi_df = bmi_df.sort_values('timestamp')

# Display table
st.subheader('BMI Verlauf')
st.dataframe(bmi_df)

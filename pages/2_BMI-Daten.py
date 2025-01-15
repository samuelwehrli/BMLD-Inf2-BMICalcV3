import streamlit as st
import pandas as pd
from utils.app_manager import AppManager
from functions.bmi_data_manager import load_bmi_data

app_manager = AppManager()
app_manager.login_page()

st.title('BMI Werte')

bmi_df = load_bmi_data()
if bmi_df.empty:
    st.info('Keine BMI Daten vorhanden. Berechnen Sie Ihren BMI auf der Startseite.')
    st.stop()

# Sort dataframe by timestamp
bmi_df = bmi_df.sort_values('timestamp', ascending=False)

# Display table
st.dataframe(bmi_df)

import streamlit as st
import pandas as pd
from utils.app_manager import AppManager
from functions.bmi_data_manager import load_bmi_data

app_manager = AppManager()
app_manager.login_page()

st.title('BMI Verlauf')

bmi_df = load_bmi_data()
if bmi_df.empty:
    st.info('Keine BMI Daten vorhanden. Berechnen Sie Ihren BMI auf der Startseite.')
    st.stop()

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




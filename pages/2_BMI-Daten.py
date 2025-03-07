import streamlit as st
from utils.login_manager import LoginManager

LoginManager().go_to_login('Start.py')  # redirect to login page if no user is logged in

st.title('BMI Werte')

bmi_df = st.session_state['bmi_df']
if bmi_df.empty:
    st.info('Keine BMI Daten vorhanden. Berechnen Sie Ihren BMI auf der Startseite.')
    st.stop()

# Sort dataframe by timestamp
bmi_df = bmi_df.sort_values('timestamp', ascending=False)

# Display table
st.dataframe(bmi_df)

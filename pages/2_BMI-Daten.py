import streamlit as st

# redirect to login page if no user is logged in
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py')  

st.title('BMI Werte')

data_df = st.session_state['data_df']
if data_df.empty:
    st.info('Keine BMI Daten vorhanden. Berechnen Sie Ihren BMI auf der Startseite.')
    st.stop()

# Sort dataframe by timestamp
data_df = data_df.sort_values('timestamp', ascending=False)

# Display table
st.dataframe(data_df)

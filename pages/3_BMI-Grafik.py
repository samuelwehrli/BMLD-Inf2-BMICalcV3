import streamlit as st
from utils.login_manager import LoginManager

LoginManager().login()  # login page

st.title('BMI Verlauf')

bmi_df = st.session_state['bmi_df']
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




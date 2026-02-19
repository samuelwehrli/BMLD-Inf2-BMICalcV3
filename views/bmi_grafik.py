import streamlit as st

st.title('BMI Verlauf')

data_df = st.session_state['data_df']
if data_df.empty:
    st.info('Keine BMI Daten vorhanden. Berechnen Sie Ihren BMI auf der Startseite.')
    st.stop()

# Weight over time
st.line_chart(data=data_df.set_index('timestamp')['weight'])
st.caption('Gewicht über Zeit (kg)')

# Height over time
st.line_chart(data=data_df.set_index('timestamp')['height'])
st.caption('Größe über Zeit (m)')

# BMI over time
st.line_chart(data=data_df.set_index('timestamp')['bmi'])
st.caption('BMI über Zeit')

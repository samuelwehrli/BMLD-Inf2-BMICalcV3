import streamlit as st
from functions.bmi_calculator import calculate_bmi
from utils.data_manager import DataManager

st.title('BMI Rechner')

with st.form("BMI Eingabeformular"):
    height = st.number_input('Geben Sie Ihre Größe ein (in Meter)', min_value=0.1, max_value=3.0, value=1.7, step=0.01)
    weight = st.number_input('Geben Sie Ihr Gewicht ein (in kg)', min_value=1.0, max_value=500.0, value=70.0, step=0.1)
    submitted = st.form_submit_button("Submit")

if submitted:
    result = calculate_bmi(height, weight)
    st.write(f'Ihr BMI ist: {result["bmi"]}')
    st.write(f'Kategorie: {result["category"]}')

    dm = DataManager()
    st.session_state['data_df'] = dm.append_record(st.session_state['data_df'], result)
    dm.save_user_data(st.session_state['data_df'], 'data.csv')

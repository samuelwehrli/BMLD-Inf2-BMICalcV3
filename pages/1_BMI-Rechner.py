import streamlit as st
import pandas as pd
from utils.app_manager import AppManager
from functions.bmi_calculator import calculate_bmi
from functions.bmi_data_manager import update_bmi_data

app_manager = AppManager()
app_manager.check_login()

bmi_file = app_manager.get_user_data_file('bmi.csv')

st.title('BMI Rechner')

# Get user input for height and weight
height = st.number_input('Geben Sie Ihre Größe ein (in Meter)', min_value=0.1, max_value=3.0, value=1.7, step=0.01)
weight = st.number_input('Geben Sie Ihr Gewicht ein (in kg)', min_value=1.0, max_value=500.0, value=70.0, step=0.1)

# Calculate BMI when button is clicked
if st.button('BMI berechnen'):

    result = calculate_bmi(height, weight)
    
    st.write(f'Ihr BMI ist: {result["bmi"]}')
    st.write(f'Berechnet am: {result["timestamp"]}')
    st.write(f'Kategorie: {result["category"]}')
        
    # Add some health advice
    st.info('Der BMI ist ein Screening-Tool, aber keine Diagnose für Körperfett oder Gesundheit. Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.')

    if update_bmi_data(bmi_file, result):
        st.success('BMI Daten wurden erfolgreich gespeichert.')
    else:
        st.error('Fehler beim Speichern der BMI Daten.')
        
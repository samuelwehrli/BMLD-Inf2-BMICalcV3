import streamlit as st
from utils.app_manager import AppManager

app_manager = AppManager(storage_type='switchdrive', login_py_file='Start.py')
app_manager.login_page(show_register_tab=True)

st.title('BMI Rechner')

st.markdown("""
Diese App wurde von Samuel Wehrli im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.

Die Anwendung ermöglicht es Ihnen, Ihren BMI zu berechnen und im Zeitverlauf zu verfolgen.
""")
        
# Add some health advice
st.info('Der BMI ist ein Screening-Tool, aber keine Diagnose für Körperfett oder Gesundheit. Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.')

        
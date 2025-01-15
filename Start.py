import streamlit as st
from utils.app_manager import AppManager

app_manager = AppManager(fs_protocol='webdav', fs_root_folder="App/BMLD-Inf2-BMICalcV3")
app_manager.login_page(show_register_tab=True)

st.title('BMI Rechner')

name = st.session_state.get('name')
st.write(f"Hallo {name}!")
st.write("Die Anwendung ermöglicht es Ihnen, Ihren BMI zu berechnen und im Zeitverlauf zu verfolgen.")
        
# Add some health advice
st.info("""Der BMI ist ein Screening-Tool, aber keine Diagnose für Körperfett oder Gesundheit. 
Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.""")

st.write("Diese App wurde von Samuel Wehrli im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")
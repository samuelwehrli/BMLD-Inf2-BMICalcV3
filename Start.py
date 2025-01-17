import streamlit as st
import pandas as pd

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# initialize data manager and load persistent data
# data_manager = DataManager()  # for local use
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="App/BMLD-Inf2-BMICalcV3")  # switch drive 
data_manager.load_user_data('bmi_df','bmi.csv', pd.DataFrame(), parse_dates = ['timestamp'])

# initialize login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()

st.title('BMI Rechner')

name = st.session_state.get('name')
st.markdown(f"✨ Hallo {name}! ✨")
st.markdown("🏃 Die Anwendung ermöglicht es Ihnen, Ihren BMI zu berechnen und im Zeitverlauf zu verfolgen 📊")
        
# Add some health advice
st.info("""Der BMI ist ein Screening-Tool, aber keine Diagnose für Körperfett oder Gesundheit. 
Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.""")

st.write("Diese App wurde von Samuel Wehrli im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")
import streamlit as st

st.title('BMI Rechner')

name = st.session_state.get('name')
st.markdown(f"✨ Hallo {name}! ✨")
st.markdown("🏃 Die Anwendung ermöglicht es Ihnen, Ihren BMI zu berechnen und im Zeitverlauf zu verfolgen 📊")

st.info("""Der BMI ist ein Screening-Tool, aber keine Diagnose für Körperfett oder Gesundheit.
Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.""")

st.write("Diese App wurde von Samuel Wehrli im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")

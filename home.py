import streamlit as st
from functions.app_manager import AppManager

st.write(st.session_state)

app_manager = AppManager(storage_type='switchdrive')
app_manager.login_page(show_register_tab=False)


st.title('My App')





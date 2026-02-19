import pandas as pd
import streamlit as st
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

st.set_page_config(page_title="BMI Rechner", page_icon=":material/monitor_weight:")

data_manager = DataManager(fs_protocol='webdav', fs_root_folder="BMLD_App_DB")
login_manager = LoginManager(data_manager)
login_manager.login_register()  # handles login navigation + stops if not logged in

# ---- Only reached when logged in ----

if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',
        initial_value=pd.DataFrame(),
        parse_dates=['timestamp']
    )

pg_home    = st.Page("views/home.py",        title="Home",        icon=":material/home:",           default=True)
pg_rechner = st.Page("views/bmi_rechner.py", title="BMI Rechner", icon=":material/monitor_weight:")
pg_daten   = st.Page("views/bmi_daten.py",   title="BMI Daten",   icon=":material/table:")
pg_grafik  = st.Page("views/bmi_grafik.py",  title="BMI Grafik",  icon=":material/show_chart:")

pg = st.navigation([pg_home, pg_rechner, pg_daten, pg_grafik])
pg.run()

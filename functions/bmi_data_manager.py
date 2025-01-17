import pandas as pd
import streamlit as st
from utils.data_manager import DataManager

BMI_FILE = 'bmi.csv'

def update_bmi_data(bmi_result):
    """
    Update the BMI data in session state and storage with a new BMI measurement result.

    This function requires that 'bmi_df' exists in Streamlit's session state before calling.
    It appends the new measurement to the existing DataFrame and saves it to storage.

    Args:
        bmi_result (dict): A dictionary containing the BMI measurement data with keys:
            - timestamp (str): The date and time of the measurement
            - height (float): The person's height in meters
            - weight (float): The person's weight in kilograms
            - bmi (float): The calculated BMI value
            - category (str): The BMI category (e.g., 'Normal', 'Overweight')
    """
    bmi_df = st.session_state['bmi_df']

    # Append new result to dataframe 
    bmi_df = pd.concat([bmi_df, pd.DataFrame([bmi_result])], ignore_index=True)

    # write back to session state
    st.session_state['bmi_df'] = bmi_df

    # backup data in data persistent data storage
    DataManager().save_data('bmi_df')
    

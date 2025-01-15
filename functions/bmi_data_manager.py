import pandas as pd
from utils.app_manager import AppManager

BMI_FILE = 'bmi.csv'

def load_bmi_data():
    """
    Retrieves the BMI measurement data for the current user.

    Returns:
        pandas.DataFrame: DataFrame containing BMI measurements.
        Returns empty DataFrame if no data exists.
    """
    data_handler = AppManager().get_user_data_handler()
    bmi_df = data_handler.load(BMI_FILE, initial_value=pd.DataFrame(), parse_dates=['timestamp'])
    return bmi_df

def save_bmi_data(bmi_df):
    """
    Saves the BMI measurement data for the current user.
    """
    data_handler = AppManager().get_user_data_handler()
    data_handler.save(BMI_FILE, bmi_df)

def update_bmi_data(bmi_result):
    """
    Updates the BMI data storage with a new BMI measurement result.

    Args:
        bmi_result (dict): Dictionary containing the BMI measurement data with:
            - timestamp (str): Measurement date and time
            - height (float): Person's height in meters
            - weight (float): Person's weight in kilograms
            - bmi (float): Calculated BMI value
            - category (str): BMI category (e.g. 'Normal', 'Overweight')

    Returns:
        bool: True if data was saved successfully, False otherwise
    """
    bmi_df = load_bmi_data()

    # Append new result to dataframe 
    bmi_df = pd.concat([bmi_df, pd.DataFrame([bmi_result])], ignore_index=True)
    
    # Save updated dataframe
    save_bmi_data(bmi_df)
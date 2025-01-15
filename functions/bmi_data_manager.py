import pandas as pd
from utils.app_manager import AppManager

def load_bmi_df(bmi_file):
    """
    Load BMI data from file or create empty DataFrame if file doesn't exist.

    Args:
        bmi_file (CloudFile): CloudFile instance for BMI data storage.

    Returns:
        pd.DataFrame: DataFrame containing BMI records or empty DataFrame if file doesn't exist.
    """
    if bmi_file.exists():
        bmi_df = bmi_file.load()
    else:
        bmi_df = pd.DataFrame()  # create empty dataframe if file does not exist
    return bmi_df

def update_bmi_data(bmi_result, bmi_file = 'bmi.csv'):
    """
    Update BMI data file with new result.

    Args:
        bmi_file (CloudFile): CloudFile instance for BMI data storage.
        bmi_result (dict): Dictionary containing new BMI calculation result with keys:
            - timestamp (str): Date and time of measurement
            - height (float): Height in meters
            - weight (float): Weight in kilograms 
            - bmi (float): Calculated BMI value
            - category (str): BMI category classification

    Returns:
        bool: True if save was successful, False otherwise
    """
    data_handler = AppManager().get_user_data_handler()
    bmi_df = data_handler.load('bmi.csv', initial_value=pd.DataFrame())

    # Append new result to dataframe 
    bmi_df = pd.concat([bmi_df, pd.DataFrame([bmi_result])], ignore_index=True)
    
    # Save updated dataframe
    data_handler.save(bmi_file, bmi_df)
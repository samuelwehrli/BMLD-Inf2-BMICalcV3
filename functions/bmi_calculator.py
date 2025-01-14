from datetime import datetime
from zoneinfo import ZoneInfo

def calculate_bmi(height, weight, timezone='Europe/Zurich'):
    """
    Calculate BMI and return a dictionary with inputs, BMI, category, and timestamp.

    Args:
        height (float): Height in meters.
        weight (float): Weight in kilograms.

    Returns:
        dict: A dictionary containing the inputs, calculated BMI, category, and timestamp.
    """
    if height <= 0 or weight <= 0:
        raise ValueError("Height and weight must be positive values.")

    bmi = weight / (height ** 2)
    
    timestamp = datetime.now(tz=ZoneInfo(timezone)).strftime("%d.%m.%Y %H:%M:%S")

    if bmi < 18.5:
        category = 'Untergewicht'
    elif bmi < 25:
        category = 'Normalgewicht'
    elif bmi < 30:
        category = 'Übergewicht'
    else:
        category = 'Adipositas'

    return {
        "timestamp": timestamp, 
        "height": height,
        "weight": weight,
        "bmi": round(bmi, 1),
        "category": category,
    } 
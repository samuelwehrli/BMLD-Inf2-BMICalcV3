import pytest, tomllib
import pandas as pd
from functions.switchdrive import SwitchDrive
from functions.cloud_file import CloudFile

# Load credentials from secrets file
with open('.streamlit/secrets.toml', 'rb') as f:
    secrets = tomllib.load(f)
    
USERNAME = secrets["switchdrive"]["username"]
PASSCODE = secrets["switchdrive"]["passcode"]
TEST_DIR = "/test_integration"  # Dedicated test directory

@pytest.fixture
def switch_drive():
    drive = SwitchDrive(
        username=USERNAME,
        passcode=PASSCODE,
        root_path=TEST_DIR
    )
    # Ensure the test directory exists
    drive.ensure_directory_exists("")
    return drive

def test_text_file_operations(switch_drive):
    """Test operations on text files using CloudFile"""
    filename = "test.txt"
    content = "This is a test content for a text file."
    
    cloud_file = CloudFile(path=filename, storage=switch_drive)
    
    # Save content to the file
    assert cloud_file.save(content)
    
    # Check if the file exists
    assert cloud_file.exists()
    
    # Load and verify content
    loaded_content = cloud_file.load()
    assert loaded_content == content
    
    # Delete the file
    assert cloud_file.delete()
    assert not cloud_file.exists()

def test_json_file_operations(switch_drive):
    """Test operations on JSON files using CloudFile"""
    filename = "test.json"
    data = {"key": "value", "number": 42}
    
    cloud_file = CloudFile(path=filename, storage=switch_drive)
    
    # Save JSON data to the file
    assert cloud_file.save(data)
    
    # Check if the file exists
    assert cloud_file.exists()
    
    # Load and verify JSON data
    loaded_data = cloud_file.load()
    assert loaded_data == data
    
    # Delete the file
    assert cloud_file.delete()
    assert not cloud_file.exists()

def test_dataframe_file_operations(switch_drive):
    """Test operations on DataFrame files using CloudFile"""
    filename = "test.csv"
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    
    cloud_file = CloudFile(path=filename, storage=switch_drive)
    
    # Save DataFrame to the file
    assert cloud_file.save(df)
    
    # Check if the file exists
    assert cloud_file.exists()
    
    # Load and verify DataFrame
    loaded_df = cloud_file.load()
    pd.testing.assert_frame_equal(loaded_df, df)
    
    # Delete the file
    assert cloud_file.delete()
    assert not cloud_file.exists() 
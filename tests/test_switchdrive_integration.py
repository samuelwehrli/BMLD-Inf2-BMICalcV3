import pytest
import pandas as pd
import tomllib
import os
from functions.switchdrive import SwitchDrive

# Load credentials
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
    
    # First, verify authentication works
    if not drive.session.get(drive.webdav_url).ok:
        pytest.fail("Authentication failed. Check your credentials.")
    
    # Ensure test directory exists by trying to create it
    try:
        # Create test directory if it doesn't exist
        drive.session.request(
            'MKCOL',
            drive._full_path("")
        )
    except Exception as e:
        print(f"Warning: Could not create test directory: {e}")
    
    # Clean up test directory before each test
    if drive.file_exists(TEST_DIR):
        for file in drive.list_files(TEST_DIR):
            drive.delete_file(file)
    return drive

def test_text_operations(switch_drive):
    """Test writing and reading text files"""
    test_content = "Hello, this is a test content!"
    filename = "test.txt"
    
    # Write text
    assert switch_drive.write_text(filename, test_content)
    
    # Verify file exists
    assert switch_drive.file_exists(filename)
    
    # Read and verify content
    read_content = switch_drive.read_text(filename)
    assert read_content == test_content
    
    # Clean up
    assert switch_drive.delete_file(filename)

def test_error_handling(switch_drive):
    """Test error cases"""
    nonexistent_file = f"{TEST_DIR}/nonexistent.txt"
    
    # Test reading non-existent file
    with pytest.raises((FileNotFoundError, Exception)) as exc_info:
        switch_drive.read_text(nonexistent_file)
    
    # Test deleting non-existent file
    result = switch_drive.delete_file(nonexistent_file)
    assert not result, f"Delete of non-existent file {nonexistent_file} should return False"
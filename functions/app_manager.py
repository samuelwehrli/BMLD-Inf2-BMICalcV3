import secrets
import streamlit as st
from functions.switchdrive import SwitchDrive
from functions.cloud_file import CloudFile
from functions.login_manager import LoginManager

class AppManager:
    """A class to manage application state, storage, and authentication."""
    
    def __init__(self, **app_manager_config):
        """Initialize the AppManager with configuration.
        
        Args:
            **app_manager_config: Arbitrary keyword arguments for configuration.
                Must include 'storage_type' if no existing configuration exists.
        
        Raises:
            ValueError: If no configuration is provided and none exists in session state.
        """
        if self._get_app_manager_data() is not None:
            return
        elif len(app_manager_config) > 0:
            self._init_app_manager_data(**app_manager_config)
        else:
            raise ValueError("AppManager: No configuration provided and no configuration found in session state")

    @staticmethod
    def _get_secret(*keys, default_value = None):
        """Retrieve a secret value from Streamlit's secrets management.
        
        Args:
            *keys: Variable length sequence of keys to access nested secrets.
            default_value: Optional default value if key is not found.
        
        Returns:
            The secret value at the specified key path.
            
        Raises:
            ValueError: If key not found and no default_value provided.
        """
        recursive_secrets = st.secrets
        for key in keys:
            if key not in recursive_secrets and default_value is None:
                raise ValueError(f"AppManager: No {key} found in streamlit secrets")
            elif key not in recursive_secrets and default_value is not None:
                return default_value
            else:
                recursive_secrets = recursive_secrets[key]
        return recursive_secrets

    def _init_app_manager_data(self, 
                               storage_type: str, 
                               credentials_file_name = 'credentials.csv',
                               cookie_name = 'bmld_inf2_streamlit_app'):
        """Initialize the application manager data with specified storage type.
        
        Args:
            storage_type (str): Type of storage to use (e.g. 'switchdrive')
            
        Raises:
            ValueError: If storage_type is not supported.
        """
        app_manager_data = {
            'storage_type': storage_type,
        }

        if storage_type == 'switchdrive':
            app_drive = SwitchDrive(
                username = self._get_secret('switchdrive', 'username'),
                passcode = self._get_secret('switchdrive', 'passcode'),
                root_path = self._get_secret('switchdrive', 'root_path', default_value = '')
            )
        else:
            raise ValueError(f"AppManager: Invalid storage type: {storage_type}")

        credentials_file = CloudFile(credentials_file_name, app_drive)
        login_manager = LoginManager(credentials_file, cookie_name, secrets.token_urlsafe(32))

        app_manager_data['app_drive'] = app_drive
        app_manager_data['login_manager'] = login_manager
        
        st.session_state['app_manager'] = app_manager_data

    @staticmethod
    def _get_app_manager_data():
        """Get the application manager data from session state.
        
        Returns:
            dict: The app manager data dictionary, or None if not initialized.
        """
        return st.session_state.get('app_manager', None)

    @staticmethod
    def _save_app_manager_data(self):
        """Save the current app manager data to session state."""
        st.session_state['app_manager'] = self.app_manager_data

    def check_login(self, login_page_py_file):
        """Check login status and handle authentication flow.
        
        Creates a logout button that logs the user out and redirects to the login page.
        If the user is not logged in, the login page is displayed.

        Args:
            login_page_py_file (str): The path to the Python file containing the login page
        """
        if st.session_state.get("authentication_status") is not True:
            st.switch_page(login_page_py_file)
        else:
            app_manager_data = self._get_app_manager_data()
            login_manager = app_manager_data['login_manager']
            login_manager.logout() # create logout button

    def get_current_user(self):
        return st.session_state.get('username', None)

    def get_user_data_file(self, file_name):
        """Get a CloudFile instance for user-specific data storage.
        
        Args:
            file_name (str): Name of the file to access
            
        Returns:
            CloudFile: A CloudFile instance for the specified user data file
            
        Raises:
            ValueError: If no user is currently logged in
        """
        user = st.session_state.get('username', None)
        if user is None:
            raise ValueError("AppManager: No user logged in")
        else:
            app_manager_data = self._get_app_manager_data()
            app_drive = app_manager_data['app_drive']
            user_data_folder = 'user_data_' + user
            drive = app_drive.get_subfolder_drive(user_data_folder)
            return CloudFile(file_name, drive)

    def get_app_data_file(file_name): 
        """Get a CloudFile instance for application-wide data storage.
        
        Args:
            file_name (str): Name of the file to access
            
        Returns:
            CloudFile: A CloudFile instance for the specified app data file
        """
        app_manager_data = self._get_app_manager_data()
        app_drive = app_manager_data['app_drive']
        app_data_folder = 'app_data'
        drive = app_drive.get_subfolder_drive(app_data_folder)
        return CloudFile(file_name, drive)

    def login_page(self, show_register_tab = True):
        """Display the login page and handle user authentication.
        
        Args:
            show_register_tab (bool): Whether to show the registration tab.
                Defaults to True.
        """
        app_manager_data = self._get_app_manager_data()
        login_manager = app_manager_data['login_manager']
        login_manager.login_page(show_register_tab)


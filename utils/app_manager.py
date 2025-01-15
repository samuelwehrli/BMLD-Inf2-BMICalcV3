import secrets, fsspec, posixpath
import streamlit as st
import streamlit_authenticator as stauth
from utils.data_handler import DataHandler


class AppManager:
    """
    Singleton class that manages application state, storage, and user authentication.
    
    Handles filesystem access, user credentials, and authentication state using Streamlit's
    session state for persistence across reruns. Provides interfaces for accessing user-specific
    and application-wide data storage.
    """
    def __new__(cls, *args, **kwargs):
        """
        Implements singleton pattern by returning existing instance from session state if available.

        Returns:
            AppManager: The singleton instance, either existing or newly created
        """
        if 'app_manager' in st.session_state:
            return st.session_state.app_manager
        else:
            instance = super(AppManager, cls).__new__(cls)
            st.session_state.app_manager = instance
            return instance
    
    def __init__(self, fs_protocol: str = None, 
                 fs_root_folder: str = None,
                 auth_credentials_file: str = 'credentials.yaml',
                 auth_cookie_name: str = 'bmld_inf2_streamlit_app'):
        """
        Initializes filesystem and authentication components if not already initialized.

        Sets up filesystem access using the specified protocol and configures authentication
        with cookie-based session management.

        Args:
            fs_protocol: Filesystem protocol to use ('webdav' or 'file')
            fs_root_folder: Base directory for all file operations
            auth_credentials_file: YAML file path for storing user credentials
            auth_cookie_name: Name for the authentication cookie
        """
        if hasattr(self, 'fs'):  # check if instance is already initialized
            return

        for var in [fs_protocol, fs_root_folder]:
            if var is None:
                raise ValueError(f"AppManager: {var} is not set")
            
        # initialize filesystem stuff
        self.fs_root_folder = fs_root_folder
        self.fs = self._init_filesystem(fs_protocol)

        # initialize streamlit authentication stuff
        self.auth_credentials_file = auth_credentials_file
        self.auth_cookie_name = auth_cookie_name
        self.auth_cookie_key = secrets.token_urlsafe(32)
        self.auth_credentials = self._load_auth_credentials()
        self.authenticator = stauth.Authenticate(self.auth_credentials, self.auth_cookie_name, self.auth_cookie_key)


    @staticmethod
    def _init_filesystem(protocol: str):
        """
        Creates and configures an fsspec filesystem instance.

        Supports WebDAV protocol using credentials from Streamlit secrets, and local filesystem access.
        
        Args:
            protocol: The filesystem protocol to initialize ('webdav' or 'file')
            
        Returns:
            fsspec.AbstractFileSystem: Configured filesystem instance
            
        Raises:
            ValueError: If an unsupported protocol is specified
        """
        if protocol == 'webdav':
            secrets = st.secrets['webdav']
            return fsspec.filesystem('webdav', 
                                     base_url=secrets['base_url'], 
                                     auth=(secrets['username'], secrets['password']))
        elif protocol == 'file':
            return fsspec.filesystem('file')
        else:
            raise ValueError(f"AppManager: Invalid filesystem protocol: {protocol}")

    def _get_data_handler(self, subfolder: str = None):
        """
        Creates a DataHandler instance for the specified subfolder.

        Args:
            subfolder: Optional subfolder path relative to root folder

        Returns:
            DataHandler: Configured for operations in the specified folder
        """
        if subfolder is None:
            return DataHandler(self.fs, self.fs_root_folder)
        else:
            return DataHandler(self.fs, posixpath.join(self.fs_root_folder, subfolder))

    def _load_auth_credentials(self):
        """
        Loads user credentials from the configured credentials file.

        Returns:
            dict: User credentials, defaulting to empty usernames dict if file not found
        """
        dh = self._get_data_handler()
        return dh.load(self.auth_credentials_file, initial_value= {"usernames": {}})

    def _save_auth_credentials(self):
        """
        Saves current user credentials to the credentials file.
        """
        dh = self._get_data_handler()
        dh.save(self.auth_credentials_file, self.auth_credentials)

    def login_page(self, show_register_tab = False):
        """
        Renders the authentication interface.
        
        Displays login form and optional registration form. Handles user authentication
        and registration flows. Stops further execution after rendering.
        
        Args:
            show_register_tab: If True, shows registration option alongside login
        """
        if st.session_state.get("authentication_status") is True:
            self.authenticator.logout()
            return

        if show_register_tab:
            login_tab, register_tab = st.tabs(["Login", "Register new User"])
            with login_tab:
                self._show_login()
            with register_tab:
                self._show_register()
        else:
            self._show_login()            
        st.stop()

    def _show_login(self):
        """
        Renders the login form and handles authentication status messages.
        """
        self.authenticator.login()
        if st.session_state["authentication_status"] is False:
            st.error("Username/password is incorrect")
        else:
            st.warning("Please enter your username and password")

    def _show_register(self):
        """
        Renders the registration form and handles user registration flow.
        
        Displays password requirements, processes registration attempts,
        and saves credentials on successful registration.
        """
        st.info("""
        The password must be 8-20 characters long and include at least one uppercase letter, 
        one lowercase letter, one digit, and one special character from @$!%*?&.
        """)
        res = self.authenticator.register_user()
        if res[1] is not None:
            st.success(f"User {res[1]} registered successfully")
            try:
                self._save_auth_credentials()
                st.success("Credentials saved successfully")
            except Exception as e:
                st.error(f"Failed to save credentials: {e}")

    def get_user_data_handler(self):
        """
        Creates a DataHandler for the current user's private data directory.
        
        The directory name is derived from the authenticated username.
        
        Returns:
            DataHandler: Configured for user-specific data operations
            
        Raises:
            ValueError: If no user is currently authenticated
        """
        username = st.session_state.get('username', None)
        if username is None:
            raise ValueError("AppManager: No user logged in, cannot get user data handler")

        user_data_folder = 'user_data_' + username
        return self._get_data_handler(user_data_folder)

    def get_app_data_handler(self):
        """
        Creates a DataHandler for application-wide shared data.
        
        Returns:
            DataHandler: Configured for application-wide data operations
        """
        return self._get_data_handler('app_data')


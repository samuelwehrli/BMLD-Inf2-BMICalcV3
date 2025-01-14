import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from utils.cloud_file import CloudFile

class LoginManager:
    def __init__(self, 
                 credentials_file: CloudFile,
                 cookie_name: str, 
                 cookie_key: str):
        """
        Initialize the LoginManager with credentials file and cookie settings.

        Args:
            credentials_file (CloudFile): CloudFile instance for credentials storage.
            cookie_name (str): Cookie name for session persistence.
            cookie_key (str): Secret key for cookie encryption.
        """
        self.credentials_file = credentials_file
        self.cookie_name = cookie_name
        self.cookie_key = cookie_key
        self.authenticator = self._initialize_authenticator()

    def _initialize_authenticator(self):
        """
        Initializes the Streamlit Authenticator with the credentials DataFrame.
        """
        if self.credentials_file.exists():
            credentials_df = self.credentials_file.load()
            credentials = {
                "usernames": credentials_df.set_index("username").to_dict(orient="index")
            }
        else:
            credentials = {"usernames": {}}
        return stauth.Authenticate(credentials, self.cookie_name, self.cookie_key)

    def login_page(self, show_register_tab = True):
        """
        Display the login page with login and registration tabs.
        Handles user authentication and registration.
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

    def logout(self):
        self.authenticator.logout()

    def _show_login(self):
        self.authenticator.login()
        if st.session_state["authentication_status"] is False:
            st.error("Username/password is incorrect")
        else:
            st.warning("Please enter your username and password")

    def _show_register(self):
        st.info("""
        The password must be 8-20 characters long and include at least one uppercase letter, 
        one lowercase letter, one digit, and one special character from @$!%*?&.
        """)
        res = self.authenticator.register_user()
        if res[1] is not None:
            st.success(f"User {res[1]} registered successfully")
            if self._save_credentials():
                st.success("Credentials saved successfully")
            else:
                st.error("Failed to save credentials")
                
    def _save_credentials(self):
        """
        Update the credentials DataFrame with the newly registered user.
        """
        credentials = (  # this might change upon upgrade. Needs to be checked on github
            self.authenticator.  
            authentication_controller.
            authentication_model.
            credentials
        )
        credentials_df = (
            pd.DataFrame.from_dict(credentials["usernames"], orient="index")
            .reset_index()
            .rename(columns={"index": "username"})
            .drop(columns=["logged_in"])
        )
        return self.credentials_file.save(credentials_df)


# BMLD-Inf2-BMICalcV3
Full blown example of BMI Calculator with user specific login

Link to the app: https://bmi-rechner-v3.streamlit.app


# things that can be improved
- in define a function which imports data into session_state from the filesystem

```python
data_manager.load_user_data('bmi_df', 'bmi.csv', initial_value=pd.DataFrame)

data_manager.save_user_data()

data_manager = DataManager(drive='webdav', root_folder='app')
user_manager = UserManager(data_manager)

user_manager.login_page()
user_manager.load()
user_manager.save()
```

The DataManager also stores itself in the session_state.
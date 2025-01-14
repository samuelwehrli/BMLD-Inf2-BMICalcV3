import streamlit as st
from functions.app_manager import AppManager

app_manager = AppManager()
app_manager.check_login('home.py')

st.title('My simple form')

text_file = app_manager.get_user_data_file('text_file.txt')

if text_file.exists():
    st.write(text_file.load())
else:
    st.write('No text file found')  

# Create a text input field
user_input = st.text_input("Enter some text:", key="text_input")

# Display the entered text
if user_input:
    if st.button("Save Text"):
        if text_file.save(user_input):
            st.success("Text saved successfully!")
        else:
            st.error("Failed to save text")





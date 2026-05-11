#nain App
import streamlit as st
import pandas as pd
from utils import init_csv

#page Configuration

st.set_page_config(
    page_title="User Management System",
    layout="wide",
    initial_sidebar_state="expanded"

)

#initialzing CSV
init_csv()

st.title("User Management System")
st.sidebar.title("Navigation")

#creating Navigation Buttons
if 'page' not in st.session_state:
    st.session_state.page="Login"

col1,col2 = st.columns(2)
if col1.button("Register"):
    st.session_state.page="Register"
if col2.button("Login"):
    st.session_state.page="Login"

st.sidebar.info("""
- USER ID: 4-20 Charecters
- password: 8-20 charecter with upercase and lowercase letter
- Email: Valid Format
- Phone: must be pakistani format
""")

if st.session_state.page == "Register":
    st.switch_page("pages/registration.py")

elif st.session_state.page == "App":
    st.switch_page("app.py")

else:
    st.switch_page("pages/login.py")

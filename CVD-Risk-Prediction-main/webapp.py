import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# ========================== #
# PAGE CONFIGURATION
# ========================== #
st.set_page_config(
    page_title="Cardiovascular Disease Risk Prediction",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide sidebar, hamburger menu, header, and footer
hide_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# ========================== #
# SITE CONTENT
# ========================== #
st.title("Heart Disease Risk Prediction using Machine Learning")

st.write(
    """
    Welcome to the Heart Disease Risk Prediction App.
    You can navigate to the prediction page and enter your details
    to get a risk assessment based on a trained Machine Learning model.
    """
)

if st.button("Go to Prediction Page"):
    switch_page("page_2")

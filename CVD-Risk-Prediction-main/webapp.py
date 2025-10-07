import streamlit as st
import os
from streamlit_extras.switch_page_button import switch_page

# --------------------- Page Config --------------------- #
st.set_page_config(
    page_title='Heart Disease Risk Prediction',
    initial_sidebar_state='collapsed'
)

# --------------------- Hide Sidebar, Menu, Footer --------------------- #
hide_elements = """
<style>
    div[data-testid="stSidebarNav"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display:none;}
</style>
"""
st.markdown(hide_elements, unsafe_allow_html=True)

# --------------------- Title and Abstract --------------------- #
st.title('Heart Disease Risk Prediction using Machine Learning Algorithms')

with st.expander('Abstract', expanded=False):
    st.markdown("""
    Cardiovascular diseases (CVD) remain a leading cause of death globally. 
    Machine Learning (ML) can help with early detection and prevention. 
    This study uses ML models on lifestyle factors to predict CVD risk.
    [Read Full Article](https://eajournals.org/ejcsit/wp-content/uploads/sites/21/2023/06/Integrated-Machine-Learning.pdf)
    """)

# --------------------- Button Logic --------------------- #
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

def callback():
    st.session_state.button_clicked = True

def go_back():
    st.session_state.button_clicked = False

st.subheader('Begin Risk Assessment')
if st.button('Start Assessment', on_click=callback) or st.session_state.button_clicked:
    st.markdown("""
    **Medical Disclaimer:** The contents of this website are not intended to diagnose or treat any disease. 
    Always seek advice from a qualified medical professional.
    """)
    if st.button('Agree'):
        st.session_state.button_clicked = False
        switch_page('page_2')
    st.button('Disagree', on_click=go_back)

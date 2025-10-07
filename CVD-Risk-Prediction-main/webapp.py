import streamlit as st

# ==========================
# Page configuration
# ==========================
st.set_page_config(
    page_title="Heart Disease Risk Prediction",
    initial_sidebar_state="collapsed"
)

# ==========================
# Hide sidebar, menu, footer, GitHub badge
# ==========================
hide_style = """
<style>
    div[data-testid="stSidebarNav"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK { display: none; }
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# ==========================
# Session state navigation
# ==========================
if 'page' not in st.session_state:
    st.session_state.page = 'webapp'  # default page

def go_to_page(page_name):
    st.session_state.page = page_name

# ==========================
# Page content
# ==========================
st.title('Heart Disease Risk Prediction using Machine Learning Algorithms')

st.write("""
This web application allows you to assess your risk of developing cardiovascular disease (CVD) using machine learning models.
""")

with st.expander("Abstract"):
    st.markdown("""
For a long time, Cardiovascular diseases (CVD) have been one of the leading causes of death globally...
[Read full article here](https://eajournals.org/ejcsit/wp-content/uploads/sites/21/2023/06/Integrated-Machine-Learning.pdf)
""")

st.write("")
st.write("**Medical Disclaimer:** This website is not intended to diagnose or treat any disease.")

if st.button("Begin Risk Assessment"):
    go_to_page("page_2")  # Navigate to form page

import streamlit as st
import pandas as pd
import joblib
from streamlit_extras.switch_page_button import switch_page

# ========================== #
# PAGE CONFIGURATION
# ========================== #
st.set_page_config(
    page_title="Heart Disease Risk Prediction",
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
# LOAD MODEL
# ========================== #
@st.cache_resource
def load_model():
    return joblib.load("Results/final_model")  # Make sure model exists in this path

model = load_model()

# ========================== #
# PAGE TITLE
# ========================== #
st.title("Heart Disease Risk Prediction")

if st.button("Back to Main Page"):
    switch_page("webapp")

# ========================== #
# USER INPUT FORM
# ========================== #
st.subheader("Enter Your Details")

with st.form(key="user_form"):
    name = st.text_input("Name")
    
    Age_Category = st.selectbox(
        "Age Category",
        ["Select One", "18-24", "25-29", "30-34", "35-39", "40-44",
         "45-49", "50-54", "55-59", "60-64", "65-69", "70-74",
         "75-79", "80+"]
    )

    Sex = st.selectbox("Sex", ["Select One", "Male", "Female"])
    
    Height_unit = st.selectbox("Height Unit", ["Select One", "Feet and Inches", "Centimeters"])
    if Height_unit == "Feet and Inches":
        Feet = st.number_input("Feet", min_value=3, max_value=7, step=1)
        Inches = st.number_input("Inches", min_value=0, max_value=11, step=1)
        Height_cm = ((Feet * 12) + Inches) * 2.54
    else:
        Height_cm = st.number_input("Height (cm)", min_value=25, max_value=300, step=1)

    Weight_kg = st.number_input("Weight (kg)", min_value=25, max_value=300, step=1)

    Smoking_History = st.radio(
        "Smoked at least 100 cigarettes in your life?",
        ["No", "Yes"],
        horizontal=True
    )

    General_Health = st.selectbox(
        "General Health",
        ["Select One", "Poor", "Fair", "Good", "Very Good", "Excellent"]
    )

    Checkup = st.selectbox(
        "Last routine doctor visit",
        ["Select One", "Within the past year", "Within the past 2 years",
         "Within the past 5 years", "5 or more years ago", "Never"]
    )

    Exercise = st.radio(
        "Physical activity last month?",
        ["Yes", "No"],
        horizontal=True
    )

    Depression = st.radio("Ever told you had depression?", ["No", "Yes"], horizontal=True)
    Diabetes = st.radio("Ever told you had diabetes?", ["No", "Yes"], horizontal=True)
    Arthritis = st.radio("Ever told you had arthritis?", ["No", "Yes"], horizontal=True)
    Skin_Cancer = st.radio("Ever told you had skin cancer?", ["No", "Yes"], horizontal=True)
    Other_Cancer = st.radio("Ever told you had other cancer?", ["No", "Yes"], horizontal=True)

    Alcohol_Consumption = st.slider(
        "Alcohol consumption in past 30 days (days)", 0, 30, step=1
    )

    Fruit_Consumption = st.number_input("Fruit consumption (times per month)", min_value=0, max_value=120, step=1)
    Green_Vegetables_Consumption = st.number_input("Green vegetables consumption (times per month)", min_value=0, max_value=120, step=1)
    FriedPotato_Consumption = st.number_input("Fried potato consumption (times per month)", min_value=0, max_value=120, step=1)

    submit = st.form_submit_button("Predict")

# ========================== #
# MAKE PREDICTION
# ========================== #
if submit:
    try:
        BMI = Weight_kg / (Height_cm / 100) ** 2

        user_data = pd.DataFrame([[
            General_Health, Checkup, Exercise, Skin_Cancer, Other_Cancer,
            Depression, Diabetes, Arthritis, Sex, Age_Category,
            Height_cm, Weight_kg, BMI, Smoking_History,
            Alcohol_Consumption, Fruit_Consumption, Green_Vegetables_Consumption,
            FriedPotato_Consumption
        ]], columns=[
            "General_Health", "Checkup", "Exercise", "Skin_Cancer", "Other_Cancer",
            "Depression", "Diabetes", "Arthritis", "Sex", "Age_Category",
            "Height_(cm)", "Weight_(kg)", "BMI", "Smoking_History",
            "Alcohol_Consumption", "Fruit_Consumption", "Green_Vegetables_Consumption",
            "FriedPotato_Consumption"
        ])

        pred = model.predict(user_data)[0]
        pred_proba = model.predict_proba(user_data)[0]

        st.write(f"Hello, {name}!")
        st.write("Your risk of developing Cardiovascular Disease (CVD) is:")

        if pred == 0:
            st.success("LOW")
        else:
            st.error("HIGH")

        st.info(f"Probability of CVD: {pred_proba[1]:.2f}")

        st.warning(
            "Disclaimer: This prediction is based on a trained ML model and is "
            "not a medical diagnosis. Always consult your doctor for health advice."
        )

    except Exception as e:
        st.error(f"Error: Enter valid inputs. Details: {e}")

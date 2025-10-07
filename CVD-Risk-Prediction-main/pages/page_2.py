import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ==========================
# Page configuration
# ==========================
st.set_page_config(
    page_title="Heart Disease Risk Prediction - Form",
    initial_sidebar_state="collapsed"
)

# ==========================
# Hide sidebar, menu, footer
# ==========================
hide_style = """
<style>
    div[data-testid="stSidebarNav"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# ==========================
# Session state navigation
# ==========================
if 'page' not in st.session_state:
    st.session_state.page = 'webapp'

def go_to_page(page_name):
    st.session_state.page = page_name

# ==========================
# Load ML model
# ==========================
@st.cache(allow_output_mutation=True)
def load_model():
    return joblib.load('Results/final_model')

model = load_model()

# ==========================
# Back to Main Page
# ==========================
if st.button("Main Page"):
    go_to_page("webapp")

# ==========================
# User Form
# ==========================
st.subheader("Fill out the following to assess your CVD risk:")

name = st.text_input("Enter your name:")

Age_Category = st.selectbox("Age Category", [
    "Select One","18-24","25-29","30-34","35-39","40-44","45-49",
    "50-54","55-59","60-64","65-69","70-74","75-79","80+"
])

Sex = st.selectbox("Sex", ["Select One","Male","Female"])
Height_cm = st.number_input("Height (cm)", min_value=50, max_value=250, step=1)
Weight_kg = st.number_input("Weight (kg)", min_value=20, max_value=300, step=1)
Smoking_History = st.radio("Smoked at least 100 cigarettes in life?", ["No","Yes"], horizontal=True)

General_Health = st.selectbox("General Health", ["Select One","Poor","Fair","Good","Very Good","Excellent"])
Checkup = st.selectbox("Last routine checkup", [
    "Select One","Within the past year","Within the past 2 years",
    "Within the past 5 years","5 or more years ago","Never"
])
Exercise = st.radio("Any physical activity in past month?", ["Yes","No"], horizontal=True)

Depression = st.radio("Ever diagnosed with depression?", ["No","Yes"], horizontal=True)
Diabetes = st.radio("Ever diagnosed with diabetes?", ["No","Yes"], horizontal=True)
Arthritis = st.radio("Ever diagnosed with arthritis?", ["No","Yes"], horizontal=True)
Skin_Cancer = st.radio("Ever diagnosed with skin cancer?", ["No","Yes"], horizontal=True)
Other_Cancer = st.radio("Ever diagnosed with other cancer?", ["No","Yes"], horizontal=True)

Alcohol_Consumption = st.slider(
    "Days of alcohol consumption in past 30 days:", 0, 30, step=1
)

Fruit_Consumption = st.number_input("Number of times you eat fruit in past month:", min_value=0, max_value=100, step=1)
Green_Vegetables_Consumption = st.number_input("Green vegetables per month:", min_value=0, max_value=100, step=1)
FriedPotato_Consumption = st.number_input("Fried potatoes per month:", min_value=0, max_value=100, step=1)

# ==========================
# Predict Button
# ==========================
if st.button("Predict"):

    try:
        bmi = Weight_kg / (Height_cm/100)**2
        new_input = [
            General_Health, Checkup, Exercise, Skin_Cancer, Other_Cancer,
            Depression, Diabetes, Arthritis, Sex, Age_Category,
            Height_cm, Weight_kg, bmi, Smoking_History,
            Alcohol_Consumption, Fruit_Consumption,
            Green_Vegetables_Consumption, FriedPotato_Consumption
        ]

        df = pd.DataFrame([new_input], columns=[
            'General_Health','Checkup','Exercise','Skin_Cancer','Other_Cancer',
            'Depression','Diabetes','Arthritis','Sex','Age_Category',
            'Height_(cm)','Weight_(kg)','BMI','Smoking_History',
            'Alcohol_Consumption','Fruit_Consumption',
            'Green_Vegetables_Consumption','FriedPotato_Consumption'
        ])

        pred = model.predict(df)
        y_pred_proba = model.predict_proba(df)

        st.write(f"Hello {name}!")
        risk = "LOW" if pred[0]==0 else "HIGH"
        st.success(risk) if risk=="LOW" else st.error(risk)

        st.warning("**Disclaimer:** Results are for informational purposes only. Not medical advice.")
        st.info(f"Probability of risk: {y_pred_proba[:,1][0]:.2f}")

    except Exception as e:
        st.error(f"Error: {e}")

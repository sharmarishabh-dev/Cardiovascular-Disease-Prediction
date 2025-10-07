import streamlit as st
import pandas as pd
import joblib
import os

# --------------------- Page Config --------------------- #
st.set_page_config(
    page_title='CVD Risk Assessment',
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
</style>
"""
st.markdown(hide_elements, unsafe_allow_html=True)

# --------------------- Load Model --------------------- #
@st.cache_data
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'Results', 'final_model')
    return joblib.load(model_path)

model = load_model()

# --------------------- Back to Main Page --------------------- #
if st.button('Main Page'):
    from streamlit_extras.switch_page_button import switch_page
    switch_page('webapp')

# --------------------- Form Inputs --------------------- #
st.subheader('Fill out the following:')

name = st.text_input('Enter your name:')

Age_Category = st.selectbox('Age Category', 
                            ['Select One','18-24','25-29','30-34','35-39','40-44',
                             '45-49','50-54','55-59','60-64','65-69','70-74','75-79','80+'])
Sex = st.selectbox('Sex', ['Select One','Male','Female'])
Height_cm = st.number_input('Height (cm)', min_value=25, max_value=300, step=1)
Weight_kg = st.number_input('Weight (kg)', min_value=25, max_value=300, step=1)

Smoking_History = st.radio('Have you smoked at least 100 cigarettes in your entire life?', 
                           ['No','Yes'], horizontal=True)

General_Health = st.selectbox('General Health', ['Select One','Poor','Fair','Good','Very Good','Excellent'])
Checkup = st.selectbox('Last routine doctor visit', 
                       ['Select One','Within the past year','Within the past 2 years','Within the past 5 years','5 or more years ago','Never'])
Exercise = st.radio('Did you exercise in the past month?', ['Yes','No'], horizontal=True)

Depression = st.radio('Ever diagnosed with depression?', ['No','Yes'], horizontal=True)
Diabetes = st.radio('Ever diagnosed with diabetes?', ['No','Yes'], horizontal=True)
Arthritis = st.radio('Ever diagnosed with arthritis?', ['No','Yes'], horizontal=True)
Skin_Cancer = st.radio('Ever diagnosed with skin cancer?', ['No','Yes'], horizontal=True)
Other_Cancer = st.radio('Ever diagnosed with other cancer?', ['No','Yes'], horizontal=True)

Alcohol_Consumption = st.slider('Days with at least one alcoholic drink in past 30 days', 0, 30, step=1)

Fruit_Consumption = st.number_input('Number of fruit servings per month', min_value=0, max_value=100, step=1)
Green_Vegetables_Consumption = st.number_input('Number of green vegetable servings per month', min_value=0, max_value=100, step=1)
FriedPotato_Consumption = st.number_input('Number of fried potato servings per month', min_value=0, max_value=100, step=1)

submit = st.button('Predict')

# --------------------- Prediction --------------------- #
if submit:
    try:
        bmi = Weight_kg / (Height_cm/100)**2

        input_data = [General_Health, Checkup, Exercise, Skin_Cancer, Other_Cancer, Depression,
                      Diabetes, Arthritis, Sex, Age_Category, Height_cm, Weight_kg, bmi,
                      Smoking_History, Alcohol_Consumption, Fruit_Consumption,
                      Green_Vegetables_Consumption, FriedPotato_Consumption]

        df = pd.DataFrame([input_data], columns=['General_Health','Checkup','Exercise','Skin_Cancer','Other_Cancer',
                                                 'Depression','Diabetes','Arthritis','Sex','Age_Category',
                                                 'Height_(cm)','Weight_(kg)','BMI','Smoking_History','Alcohol_Consumption',
                                                 'Fruit_Consumption','Green_Vegetables_Consumption','FriedPotato_Consumption'])

        pred = model.predict(df)
        y_proba = model.predict_proba(df)

        st.write(f'Hello, {name}!')
        st.write('Your risk of developing Cardiovascular Disease (CVD) is:')

        if pred[0] == 0:
            st.success('LOW')
        else:
            st.error('HIGH')

        st.warning('**Disclaimer:** This result is not medical advice. Only personal attributes were used for prediction.')

        details = st.expander('More Details', expanded=False)
        with details:
            st.info(f'Probability at risk: {y_proba[0][1]:.2f}')
            st.info(f'Probability not at risk: {y_proba[0][0]:.2f}')

        st.balloons()

    except Exception as e:
        st.error(f'Error: {str(e)}. Please enter valid inputs.')

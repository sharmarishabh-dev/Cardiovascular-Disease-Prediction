import streamlit as st
import joblib
import os

# ========================== #
# Load Model Safely
# ========================== #
@st.cache_resource
def load_model():
    model_path = "Results/final_model"
    
    # Optionally download from URL if model is not in repo
    # import gdown
    # url = "YOUR_FILE_LINK"
    # if not os.path.exists(model_path):
    #     gdown.download(url, model_path, quiet=False)
    
    if not os.path.exists(model_path):
        st.error(f"Model file not found at '{model_path}'. Please make sure it exists in the repo.")
        return None
    return joblib.load(model_path)

model = load_model()

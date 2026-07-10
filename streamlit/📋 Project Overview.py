# --------------------------------------------------
# Import Modules
# --------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pickle as pkl

# --------------------------------------------------
# Load Models and Encoders
# --------------------------------------------------

with open("../encoded_files/company_tier_encoder.pkl", "rb") as file:
    company_tier_encoder = pkl.load(file)

with open("../encoded_files/competition_level_encoder.pkl", "rb") as file:
    competition_level_encoder = pkl.load(file)

with open("../encoded_files/degree_spec_encoder.pkl", "rb") as file:
    degree_spec_encoder = pkl.load(file)

with open("../encoded_files/label_encoders.pkl", "rb") as file:
    label_encoders = pkl.load(file)

with open("../encoded_files/scaler.pkl", "rb") as file:
    scaler = pkl.load(file)

with open("../encoded_files/ml_model.pkl", "rb") as file:
    xg_boost_model = pkl.load(file)


# --------------------------------------------------
# Configuring Streamlit Page
# --------------------------------------------------

st.set_page_config(
    page_title="Job Acceptance Prediction System",
    page_icon="💼",
    layout="wide"
)

# --------------------------------------------------
# Project Overview Page
# --------------------------------------------------


st.title("📋 Streamlit App for Job Prediction System")

st.subheader("Project Name")

st.write("* Job Acceptance Prediction System")

st.subheader("Objective")

st.write("The Job Acceptance Prediction System is a machine learning application developed\
            to predict whether a candidate is likely to be placed or not placed based on\
            interview performance, aptitude scores, and other evaluation metrics.")

st.subheader("Key Features")

st.markdown("""
            - Candidate placement prediction.
            - Intractive prediction interface.
            - Data visualization and analysis dashboard.
""")


st.subheader("Technologies and Tools Used")

st.markdown("""
            - **Pandas** - Data manipulation and cleaning.
            - **Matplotlib** & Seaborn - Data visualization and analysis.
            - **SQLAlchemy** - Database connection and Storing data into MySQL.
            - **Scikit-learn** - Machine learning training and eveluation.
            - **Pickle** - Saving and loading trained machine learning model, encoders and scalers.
            - **Streamlit** - Building the intractive web application dashboard.
""")

st.subheader("Machine Learning Model")

st.markdown("""
            - Model Used: XGBoost Classifier
            - Problem Type: Binary Classification
            - Target Variable: Placement Satus(Placed or Not-Placed)
""")

st.subheader("Project Workflow")

st.markdown("""
            1. Data Collection
            2. Data Cleaning and Preprocessing
            3. Exploratory Data Analysis (EDA)
            4. Feature Engineering
            5. Train-Test Split
            6. Model Training
            7. Model Evaluation
            8. Hyperparameter Tuning and Evaluation
            9. Model storing using Pickle
            10. Streamlit Dashboard Development
""")

import pandas as pd
import pickle as pkl
import streamlit as st

# --------------------------------------------------
# Load Models and Encoders
# --------------------------------------------------

st.set_page_config(
    page_title="🎯 Job Prediction System",
    layout="wide"
)

st.title("🎯 Job Prediction System")



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
# Getting Input from User
# --------------------------------------------------

age_years = st.slider("Age", 18, 65)
gender = st.selectbox("Gender", label_encoders["gender"].classes_)

ssc_col, hsc_col, degree_col = st.columns(3)
with ssc_col:
    ssc_percentage = st.number_input(
        "SSC Percentage", 
        min_value=0.00, 
        max_value=100.00, 
        value=70.0,
        step=0.1
    )

with hsc_col:
    hsc_percentage = st.number_input(
        "HSC Percentage", 
        min_value=0.00, 
        max_value=100.00, 
        value=70.0,
        step=0.1
    )

with degree_col:
    degree_percentage = st.number_input(
        "Degree Percentage", 
        min_value=0.00, 
        max_value=100.00, 
        value=70.0,
        step=0.1
    )

# --------------------------------------------------

temp = [degree_spec_encoder.get_feature_names_out(
    ["degree_specialization"]
)][0]

degrees = list(
    map(lambda x: x.replace("degree_specialization_", ""), temp)
)


degree_specialization = st.selectbox(
    "Degree Specialization", 
    degrees
)

# --------------------------------------------------

tech_col, apt_col = st.columns(2)
with tech_col:
    technical_score = st.number_input(
        "Technical Score", 
        min_value=0.00, 
        max_value=100.00, 
        value=70.0,
        step=0.1
    )

with apt_col:
    aptitude_score = st.number_input(
        "Aptitude Score", 
        min_value=0.00, 
        max_value=100.00, 
        value=70.0,
        step=0.1
    )

# --------------------------------------------------        

comm_col, skill_match_col = st.columns(2)
with comm_col:
    communication_score = st.number_input(
        "Communication Score", 
        min_value=0.00, 
        max_value=100.00, 
        value=70.0,
        step=0.1
    )

with skill_match_col:
    skills_match_percentage = st.number_input(
        "Skill Match Percentage", 
        min_value=0.00, 
        max_value=100.00, 
        value=70.0,
        step=0.1
    )

# --------------------------------------------------

c_count_col, internship_col= st.columns(2)
with c_count_col:
    certifications_count = st.number_input(
        "Certifications Count", 
        value=1,
        step=1
    )

with internship_col:
    internship_experience = st.selectbox(
        "Internship Experience",
        label_encoders["internship_experience"].classes_
    )

# --------------------------------------------------

years_of_ex_col, career_switch_col = st.columns(2)

with years_of_ex_col:
    years_of_experience = st.number_input(
        "Years of Experience", 
        min_value=0, 
        max_value=15, 
        value=1,
        step=1
    )

with career_switch_col:
    career_switch_willingness = st.selectbox(
        "Career Switch Willingness", 
        label_encoders["career_switch_willingness"].classes_
    )

# --------------------------------------------------

relevant_exp_col, previous_ctc_col, expected_ctc_col = st.columns(3)

with relevant_exp_col:
    relevant_experience = st.selectbox(
        "Relevant Experience", 
        label_encoders["relevant_experience"].classes_
    )

with previous_ctc_col:
    previous_ctc_lpa = st.number_input(
        "Previous CTC in Lakhs", 
        min_value=0.0, 
        max_value=50.0, 
        value=5.0,
        step=0.1
    )

with expected_ctc_col:
    expected_ctc_lpa = st.number_input(
        "Expected CTC in Lakhs", 
        min_value=0.0, 
        max_value=50.0, 
        value=5.0,
        step=0.1
    )

# --------------------------------------------------

company_tier_col, job_role_match_col, competition_level_col = st.columns(3)

with company_tier_col:
    company_tier = st.selectbox(
        "Company Tier", 
        company_tier_encoder.categories_[0]
    )

with job_role_match_col:
    job_role_match = st.selectbox(
        "Job Role Match", 
        label_encoders["job_role_match"].classes_
    )

with competition_level_col:
    competition_level = st.selectbox(
        "Competition Level", 
        competition_level_encoder.categories_[0]
    )

# --------------------------------------------------

bond_col, notice_period_col, layoff_hist_col = st.columns(3)

with bond_col:
    bond_requirement = st.selectbox(
    "Bond Requirement", 
    label_encoders["bond_requirement"].classes_
)

with notice_period_col:
    notice_period_days = st.number_input(
        "Notice Period in Days", 
        min_value=0, 
        max_value=90, 
        value=10,
        step=1
    )

with layoff_hist_col:
    layoff_history = st.selectbox(
        "Layoff History", 
        label_encoders["layoff_history"].classes_
    )

# --------------------------------------------------

emp_gap_months_col, relocation_willingness_col = st.columns(2)

with emp_gap_months_col:
    employment_gap_months = st.number_input(
        "Employment Gap in Months", 
        value=10,
        step=1
    )

with relocation_willingness_col:
    relocation_willingness = st.selectbox(
        "Relocation Willingness", 
        label_encoders["relocation_willingness"].classes_
    )

# --------------------------------------------------
# Prepare input data for Prediction
# --------------------------------------------------

input_data = {
    "age_years": [age_years],
    "gender": [gender],
    "ssc_percentage": [ssc_percentage],
    "hsc_percentage": [hsc_percentage],
    "degree_percentage": [degree_percentage],
    "degree_specialization": [degree_specialization],
    "technical_score": [technical_score],
    "aptitude_score": [aptitude_score],
    "communication_score": [communication_score],
    "skills_match_percentage": [skills_match_percentage],
    "certifications_count": [certifications_count],
    "internship_experience": [internship_experience],
    "years_of_experience": [years_of_experience],
    "career_switch_willingness": [career_switch_willingness],
    "relevant_experience": [relevant_experience],
    "previous_ctc_lpa": [previous_ctc_lpa],
    "expected_ctc_lpa": [expected_ctc_lpa],
    "company_tier": [company_tier],
    "job_role_match": [job_role_match],
    "competition_level": [competition_level],
    "bond_requirement": [bond_requirement],
    "notice_period_days": [notice_period_days],
    "layoff_history": [layoff_history],
    "employment_gap_months": [employment_gap_months],
    "relocation_willingness": [relocation_willingness]
}

input_data = pd.DataFrame(input_data)

# --------------------------------------------------
# Splitting Categorize and Numeric Columns
# --------------------------------------------------

categorical_features = [
    "gender",
    "internship_experience",
    "career_switch_willingness",
    "relevant_experience",
    "job_role_match",
    "bond_requirement",
    "layoff_history",
    "relocation_willingness"
]

numeric_features = [
    "age_years",
    "ssc_percentage",
    "hsc_percentage",
    "degree_percentage",
    "technical_score",
    "aptitude_score",
    "communication_score",
    "skills_match_percentage",
    "certifications_count",
    "years_of_experience",
    "previous_ctc_lpa",
    "expected_ctc_lpa",
    "notice_period_days",
    "employment_gap_months"
]

# --------------------------------------------------
# Encoding and Scaling 
# --------------------------------------------------

# ----------- Numeric Features ---------------------

input_data[numeric_features] = scaler.transform(input_data[numeric_features])

# ------ Categorical Features - Lable Encoder ------

for column in categorical_features:
    input_data[column] = label_encoders[column].transform(input_data[column])

# --------- Company Tier - Ordinal Encoder ---------


input_data["company_tier"] = company_tier_encoder.transform(input_data[["company_tier"]])

input_data["company_tier"] = input_data["company_tier"].astype(int)

# Competition Level - Ordinal Enocder

input_data["competition_level"] = competition_level_encoder.transform(input_data[["competition_level"]])

input_data["competition_level"] = input_data["competition_level"].astype(int)

# Degree Specialization - OneHot Encoder

degree_spec_encoded = degree_spec_encoder.transform(input_data[["degree_specialization"]]).toarray()

degree_spec_encoded = pd.DataFrame(
    degree_spec_encoded, 
    columns=degree_spec_encoder.get_feature_names_out(["degree_specialization"])
)

for column in degree_spec_encoded.columns:
    degree_spec_encoded[column] = degree_spec_encoded[column].astype(int)

# Combining Table - Input and Encoded Degree Specialization

input_data = pd.concat(
    [input_data.drop(columns="degree_specialization"), degree_spec_encoded],
    axis=1
)

# --------------------------------------------------
# Prediction
# --------------------------------------------------

if st.button("Predict Job Acceptance"):
    prediction = xg_boost_model.predict(input_data)

    if prediction[0] == 1:
        st.success("Candidate Placed")
    else:
        st.error("Candidate Not-Placed")


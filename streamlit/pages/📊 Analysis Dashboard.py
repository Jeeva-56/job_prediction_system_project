import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="📊 Analysis Dashboard",
    layout="wide"
)

st.title("📊 Analysis Dashboard")
st.markdown("Candidate Placement Analytics Dashboard")

# ----------------------------------
# Load Data
# ----------------------------------

df = pd.read_csv("../csv_files/hr_job_placement_dataset_cleaned.csv")


# ----------------------------------
# Sidebar Filter
# ----------------------------------

st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Genders",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)


degree = st.sidebar.multiselect(
    "Degree Specialization",
    options=df["degree_specialization"].unique(),
    default=df["degree_specialization"].unique()
)

internship = st.sidebar.multiselect(
    "Internship Experience",
    options=df["internship_experience"].unique(),
    default=df["internship_experience"].unique()
)

relevant_exp = st.sidebar.multiselect(
    "Relevant Experience",
    options=df["relevant_experience"].unique(),
    default=df["relevant_experience"].unique()
)

status = st.sidebar.multiselect(
    "Status",
    options=df["status"].unique(),
    default=df["status"].unique()
)

# Apply Filters

filtered_df = df.copy()

filtered_df = filtered_df[
    (df["gender"].isin(gender)) & 
    (df["degree_specialization"].isin(degree)) & 
    (df["internship_experience"].isin(internship)) & 
    (df["relevant_experience"].isin(relevant_exp)) & 
    (df["status"].isin(status))
]

# ----------------------------------
# Creating KPI Values
# ----------------------------------

# Calculate Total Candicates 

total_candidate = len(filtered_df)


# Calculate Placement Rate %

placement_count = len(filtered_df[filtered_df["status"] == "Placed"])

placement_rate = (placement_count / total_candidate) * 100


# Calculate Average Interview Score

filtered_df["interview_score"] = (filtered_df["technical_score"] + filtered_df["aptitude_score"] + filtered_df["communication_score"]) / 3


avg_interview_score = filtered_df["interview_score"].mean()


# Calculate Average Skill Match % 

avg_skill_match = filtered_df["skills_match_percentage"].mean()


# Calculate High Risk Candidate % 

high_risk = filtered_df[
    (filtered_df["skills_match_percentage"] < 70) |
    (filtered_df["job_role_match"] == "Not Matched") |
    (filtered_df["employment_gap_months"] > 12)
]
high_risk_rate = (len(high_risk) / total_candidate) * 100


# ----------------------------------
# Visualize KPI Values
# ----------------------------------

(total_candidate_col, placement_count_col, placement_rate_col, \
 avg_interview_score_col, avg_skill_match_col, high_risk_rate_col) = st.columns(6) 

with total_candidate_col:
    st.metric(
        "Total Candidates",
        total_candidate,
        border=True
    )
    
with placement_count_col:
    st.metric(
        "Placement Count",
        placement_count,
        border=True
    )

with placement_rate_col:
    st.metric(
        "Placement Rate",
        f"{placement_rate:.2f} %",
        border=True
    )

with avg_interview_score_col:
    st.metric(
        "Average Interview Score",
        f"{avg_interview_score:.2f}",
        border=True
    )

with avg_skill_match_col:
    st.metric(
        "Average Skill Match Rate",
        f"{avg_skill_match:.2f} %",
        border=True
    )

with high_risk_rate_col:
    st.metric(
        "High Risk Candidate Rate",
        f"{high_risk_rate:.2f} %",
        border=True
    )




# ----------------------------------
# Creating Charts - 1
# ----------------------------------

placement_pie_col, gender_pie_col = st.columns(2)

# Placement Distribution Pie Chart
with placement_pie_col:
    with st.container(border=True):
        fig = px.pie(
            filtered_df,
            names="status",
            title="Placement Distribution"
        )

        fig.update_layout(title={
            "text": "Skill Match Percentage",
            "font": {"size": 24}
        })

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# Gender Distribution Pie Chart

with gender_pie_col:
    with st.container(border=True):
        fig = px.pie(
            filtered_df,
            names="gender",
            title="Gender Distribution"
        )

        fig.update_layout(title={
            "text": "Skill Match Percentage",
            "font": {"size": 24}
        })

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ----------------------------------
# Creating Charts - 2
# ----------------------------------

skill_match_hist, interview_score_hist  = st.columns(2)

# Skill Match Percentage Histogram

with skill_match_hist:
    with st.container(border=True):
        fig = px.histogram(
            filtered_df,
            nbins=10,
            x="skills_match_percentage",
            title="Skill Match Percentage"
        )

        fig.update_layout(title={
            "text": "Skill Match Percentage",
            "font": {"size": 24}
        })

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# Technical Score Histogram

with interview_score_hist:
    with st.container(border=True):
        fig = px.histogram(
            filtered_df,
            nbins=10,
            x="interview_score",
            title="Interview Score"
        )
        
        fig.update_layout(title={
            "text": "Interview Score",
            "font": {"size": 24}
        })

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ----------------------------------
# Creating Charts - 3
# ----------------------------------

degree_rate_col, company_tier_col = st.columns(2)

# Placement Rate By Degree Histogram

with degree_rate_col:
    with st.container(border=True):
        degree_dist = filtered_df["degree_specialization"].value_counts()

        degree_dist = pd.DataFrame({
            "degree": degree_dist.index,
            "count": degree_dist.values
        })

        degree_dist["rate"] = (degree_dist["count"] / len(filtered_df)) * 100

        fig = px.bar(
            degree_dist,
            x="degree",
            y="rate",
            title="Placement Rate By Degree",
            text="count"
            
        )

        fig.update_layout(title={
            "text": "Placement Rate By Degree",
            "font": {"size": 24}
        })

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with company_tier_col:
    with st.container(border=True):
        company_tier = filtered_df["company_tier"].value_counts()

        company_tier = pd.DataFrame({
            "tier": company_tier.index,
            "count": company_tier.values
        })

        

        fig = px.bar(
            company_tier,
            x="tier",
            y="count",
            title="Company Tier Distribution",
        )

        fig.update_layout(title={
            "text": "Company Tier Distribution",
            "font": {"size": 24}
        })

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ----------------------------------
# Visualize Dataframe
# ----------------------------------

st.subheader("Candidate Details")

st.dataframe(
    filtered_df,
    use_container_width=True
)
import streamlit as st
import pandas as pd
import os
import kagglehub

# පිටුවේ මාතෘකාව සැකසීම (Page Configuration)
st.set_page_config(page_title="Hospital Patient Records", layout="wide")

st.title("🏥 Hospital Patient Records Analysis App")
st.write("This app analyzes the Hospital Patient Records Dataset.")

# 1. Dataset එක Download කරගැනීම
@st.cache_data # App එක ඉක්මනින් load වීම සඳහා data cache කිරීම
def load_data():
    path = kagglehub.dataset_download("mmumairkhattak/hospital-patient-records-dataset-2026-healthcare")
    hospital_data_path = os.path.join(path, 'hospital_patient_records_dataset.csv')
    df = pd.read_csv(hospital_data_path)
    return df

try:
    with st.spinner("Loading dataset... Please wait."):
        df = load_data()
    st.success("Dataset loaded successfully!")

    # Sidebar - Filters සඳහා
    st.sidebar.header("Filter Options")

    # Gender Filter
    gender_list = ["All"] + list(df['Gender'].unique())
    selected_gender = st.sidebar.selectbox("Select Gender", gender_list)

    # Admission Type Filter
    admission_list = ["All"] + list(df['Admission_Type'].unique())
    selected_admission = st.sidebar.selectbox("Select Admission Type", admission_list)

    # Data Filtering
    filtered_df = df.copy()
    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_admission != "All":
        filtered_df = filtered_df[filtered_df['Admission_Type'] == selected_admission]

    # 2. Data Display කිරීම
    st.subheader("📋 Patient Data Preview")
    st.dataframe(filtered_df.head(100)) # මුල් records 100 පෙන්වීම

    # 3. මූලික සංඛ්‍යා දත්ත (Key Metrics)
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Patients (Filtered)", len(filtered_df))
    col2.metric("Average Age", f"{filtered_df['Age'].mean():.1f} Years")
    col3.metric("Average Treatment Cost", f"${filtered_df['Treatment_Cost'].mean():.2f}")

    # 4. Charts / Visualizations
    st.subheader("📈 Visualizations")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("#### Distribution of Severity Level")
        severity_counts = filtered_df['Severity_Level'].value_counts()
        st.bar_chart(severity_counts)

    with chart_col2:
        st.write("#### Treatment Outcome Breakdown")
        outcome_counts = filtered_df['Treatment_Outcome'].value_counts()
        st.bar_chart(outcome_counts)

except Exception as e:
    st.error(f"Error loading data: {e}")

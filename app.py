import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Hospital Patient Records Dashboard", layout="wide")

st.title("🏥 Hospital Patient Records Analysis (2026)")
st.write("Google Colab මඟින් විශ්ලේෂණය කරන ලද දත්ත ඇසුරෙන් සකසන ලද Dashboard එක.")

# Load the .pkl file
@st.cache_data
def load_data():
    with open('hospital_df.pkl', 'rb') as f:
        df = pickle.load(f)
    return df

try:
    df = load_data()
    
    # Sidebar Filters
    st.sidebar.header("දත්ත Filter කරන්න")
    gender = st.sidebar.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
    severity = st.sidebar.multiselect("Severity Level", options=df['Severity_Level'].unique(), default=df['Severity_Level'].unique())
    
    filtered_df = df[(df['Gender'].isin(gender)) & (df['Severity_Level'].isin(severity))]
    
    # KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("මුළු රෝගීන් ගණන", len(filtered_df))
    col2.metric("සාමාන්‍ය වයස", f"{filtered_df['Age'].mean():.1f} Years")
    col3.metric("සාමාන්‍ය ප්‍රතිකාර වියදම", f"${filtered_df['Treatment_Cost'].mean():.2f}")
    
    st.markdown("---")
    
    # Charts Section
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Gender Distribution")
        fig, ax = plt.subplots()
        sns.countplot(data=filtered_df, x='Gender', ax=ax, palette='pastel')
        st.pyplot(fig)
        
    with c2:
        st.subheader("Age Distribution")
        fig, ax = plt.subplots()
        sns.histplot(data=filtered_df, x='Age', kde=True, ax=ax, color='skyblue')
        st.pyplot(fig)
        
    st.subheader("Patient Data Table (Sample 100 rows)")
    st.dataframe(filtered_df.head(100))

except FileNotFoundError:
    st.error("කරුණාකර 'hospital_df.pkl' file එක app.py ඇති folder එක තුළටම ඇතුළත් කරන්න.")
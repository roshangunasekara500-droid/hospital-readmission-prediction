
import streamlit as st
import pandas as pd
import pickle

# Load the preprocessed DataFrame
@st.cache_data
def load_data():
    try:
        with open('hospital_df.pkl', 'rb') as f:
            df = pickle.load(f)
        return df
    except FileNotFoundError:
        st.error("Error: 'hospital_df.pkl' not found. Please ensure the file is in the same directory.")
        return pd.DataFrame()

hospital_df = load_data()

st.title('Hospital Patient Records Analysis')
st.write('A simple Streamlit application to display the hospital patient records data.')

if not hospital_df.empty:
    st.subheader('DataFrame Information')
    st.write(f"Shape of the DataFrame: {hospital_df.shape}")
    st.write(f"Columns: {', '.join(hospital_df.columns)}")

    st.subheader('First 5 Rows of the DataFrame')
    st.dataframe(hospital_df.head())

    st.subheader('Descriptive Statistics')
    st.dataframe(hospital_df.describe())
else:
    st.write("No data to display. Please make sure `hospital_df.pkl` is generated and accessible.")

import streamlit as st
import pandas as pd
import joblib

st.title("Hospital Patient Records Prediction App")

# Model එක load කිරීම
# model = joblib.load('model.pkl')

st.write("මෙය ඔබගේ පළමු Streamlit App එකයි!")

# මෙහිදී ඔබට අවශ්‍ය පරිදි user inputs ලබාගැනීමට code ලිවිය හැක.
# උදා: age = st.slider("Age", 0, 100)

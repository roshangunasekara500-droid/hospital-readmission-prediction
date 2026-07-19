import streamlit as st
import pickle
import numpy as np

# ආකෘතිය පැටවීම
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

st.title("රෝගීන් නැවත ඇතුළත් කිරීමේ අවදානම පුරෝකථනය කිරීම")

st.write("කරුණාකර රෝගියාගේ දත්ත ඇතුලත් කරන්න.")

# සටහන: ඔබගේ දත්ත කට්ටලයේ ඇති තීරු අනුව මෙහි Input fields සකස් කළ යුතුය.
# උදාහරණයක්:
# age = st.number_input("වයස", min_value=0, max_value=120, value=50)
# time_in_hospital = st.number_input("රෝහලේ ගතකළ දින ගණන", value=5)

if st.button("අවදානම පරීක්ෂා කරන්න"):
    # මෙහිදී පරිශීලකයා ඇතුලත් කළ දත්ත array එකක් ලෙස සකසා predict කළ යුතුය.
    st.success("මෙය පුරෝකථන යෙදුමේ මූලික ආකෘතියකි.")

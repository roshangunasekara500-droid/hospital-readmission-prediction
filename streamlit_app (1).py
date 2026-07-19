import streamlit as st
import pickle
import pandas as pd

# ----------------------------------------------------
# Load Pipeline and Artifacts
# ----------------------------------------------------

with open("model.pkl", "rb") as f:
    loaded_artifacts = pickle.load(f)

# Extract the full scikit-learn pipeline that includes preprocessing and the model
inference_pipeline = loaded_artifacts["pipeline"]

# Extract target classes for displaying prediction results (e.g., ['High', 'Low', 'Medium'])
target_classes = loaded_artifacts["target_classes"]

# Extract the list of original feature names that the pipeline expects as input
expected_feature_names = loaded_artifacts["feature_names"]

# Extract lists of numeric and categorical features for default value handling
numeric_features = loaded_artifacts["numeric_features"]
categorical_features = loaded_artifacts["categorical_features"]

st.title("Hospital Readmission Risk Prediction")

st.write("Enter patient information")

# ----------------------------------------------------
# Example Inputs from Streamlit UI
# ----------------------------------------------------

age = st.number_input("Age", 18, 100, 45)
gender = st.selectbox("Gender", ["Male", "Female"])
admission_type = st.selectbox(
    "Admission Type",
    ["Emergency", "Urgent", "Elective"]
)
length_of_stay = st.number_input(
    "Length of Stay",
    1,
    60,
    5
)

# ----------------------------------------------------
# Create Input DataFrame for the Pipeline
#   The pipeline expects all features present during training. Since the Streamlit
#   UI only collects a few, we need to create a DataFrame with all expected features
#   and fill in default values for the missing ones.
# ----------------------------------------------------

# Initialize a dictionary to hold the single row of input data
input_data_dict = {}

# Populate with user inputs
input_data_dict["Age"] = age
input_data_dict["Gender"] = gender
input_data_dict["Admission_Type"] = admission_type # Note: column name from training data
input_data_dict["Length_Of_Stay"] = length_of_stay # Note: column name from training data

# Fill in default values for all other expected features
# This is a basic approach; a more sophisticated app might ask for more inputs
# or use more informed defaults (e.g., mean/mode from training data).
for col in expected_feature_names:
    if col not in input_data_dict:
        if col == "Patient_ID":
            input_data_dict[col] = 0 # Dummy ID
        elif col in numeric_features:
            input_data_dict[col] = 0.0 # Default for numerical features
        elif col in categorical_features:
            # A robust solution would use the mode of the training data
            # For now, we use a placeholder that the OneHotEncoder can handle ('unknown' if configured)
            input_data_dict[col] = "Unknown" # Default for categorical features
        else:
            input_data_dict[col] = None # Fallback

# Create a Pandas DataFrame with all expected features in the correct order
user_input_df = pd.DataFrame([input_data_dict])[expected_feature_names]

# ----------------------------------------------------
# Prediction
# ----------------------------------------------------

if st.button("Predict"):
    # Use the full inference_pipeline to predict. It handles all preprocessing.
    prediction_raw = inference_pipeline.predict(user_input_df)[0]
    probability_raw = inference_pipeline.predict_proba(user_input_df)[0]

    # Map the numerical prediction index back to original class labels
    prediction_label = target_classes[prediction_raw]
    # Get probability for the predicted class
    predicted_class_probability = probability_raw[prediction_raw]

    st.subheader("Prediction")

    if prediction_label == "High":
        st.error("High Risk of Readmission")
    elif prediction_label == "Medium":
        st.warning("Medium Risk of Readmission")
    else: # "Low"
        st.success("Low Risk of Readmission")

    st.write(f"Probability of '{prediction_label}' risk: {predicted_class_probability:.2%}")

    # Optionally, show probabilities for all classes
    st.write("Probabilities for all risk levels:")
    for i, prob in enumerate(probability_raw):
        st.write(f"- {target_classes[i]}: {prob:.2%}")

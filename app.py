import joblib
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the trained model
model = joblib.load('readmission_predictor.pkl')

# If you saved a scaler, load it here as well
# scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Assuming the input 'features' are already scaled and in the correct format
    # In a real application, you would need to preprocess and scale the incoming raw data
    # For example:
    # raw_data = np.array(data['features']).reshape(1, -1)
    # scaled_data = scaler.transform(raw_data)

    # For this example, we assume `data['features']` is already a list of scaled features
    features = np.array(data['features']).reshape(1, -1)

    prediction = model.predict(features)
    prediction_proba = model.predict_proba(features)

    output = {
        'prediction': int(prediction[0]),
        'probability_no_readmission': float(prediction_proba[0][0]),
        'probability_readmission': float(prediction_proba[0][1])
    }
    return jsonify(output)

if __name__ == '__main__':
    # For local development, set debug=True
    # In production, use a production-ready WSGI server like Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)

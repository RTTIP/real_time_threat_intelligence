import joblib
import os
import numpy as np

# Load the predictive model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'predictive_model.pkl')
predictive_model = joblib.load(MODEL_PATH)

def predict_future_threat(features):
    
    feature_array = np.array([features['severity'], features['num_indicators']]).reshape(1, -1)
    prediction = predictive_model.predict(feature_array)
    return prediction[0]

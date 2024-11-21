import joblib
import numpy as np
import os

# Paths for saved models and encoders
CATEGORY_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'category_model.pkl')
RISK_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'risk_model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'label_encoder.pkl')
PREDICTIVE_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'predictive_model.pkl')

# Load models and encoders
category_model = joblib.load(CATEGORY_MODEL_PATH)
risk_model = joblib.load(RISK_MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
label_encoder = joblib.load(ENCODER_PATH)
predictive_model = joblib.load(PREDICTIVE_MODEL_PATH)

def predict_category_and_risk(threat_data):
    # Process features
    description_vector = vectorizer.transform([threat_data['description']]).toarray()[0]
    severity = threat_data.get('severity', 1)
    num_indicators = len(threat_data.get('indicators', []))

    # Combine features into a single array
    features = np.concatenate(([severity, num_indicators], description_vector))

    # Predict category and risk score
    category = category_model.predict([features])[0]
    risk_score = risk_model.predict([features])[0]

    # Decode category label
    category_label = label_encoder.inverse_transform([category])[0]
    return category_label, risk_score

def predict_future_threat(features):
    
    feature_array = np.array([features['severity'], features['num_indicators']]).reshape(1, -1)
    prediction = predictive_model.predict(feature_array)
    return prediction[0]
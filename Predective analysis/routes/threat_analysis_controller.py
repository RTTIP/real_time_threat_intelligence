from flask import Blueprint, jsonify, request
from models.predictive_model_loader import predict_future_threat


analysis_bp = Blueprint("analysis", __name__)

@analysis_bp.route('/predict_threat', methods=['POST'])
def predict_threat():
    
    # Get data from request
    data = request.json
    if not data or 'severity' not in data or 'num_indicators' not in data:
        return jsonify({"error": "Invalid input data"}), 400

    # Prepare features
    features = {
        "severity": data['severity'],
        "num_indicators": data['num_indicators']
    }

    # Get prediction
    prediction = predict_future_threat(features)
    return jsonify({"predicted_severity": prediction}), 200

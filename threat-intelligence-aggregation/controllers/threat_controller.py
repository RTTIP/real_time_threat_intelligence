from flask import request, jsonify
from models.model_loader import predict_category_and_risk, predict_future_threat
#from llm.llm_threat_summary import fetch_threat_summary, preprocess_for_llm
from app import mongo

# POST /api/v1/threats/ingest
def ingest_threat():
    data = request.get_json()
    threat = {
        "threat_id": data.get("threat_id"),
        "source": data.get("source"),
        "type": data.get("type"),
        "severity": data.get("severity"),
        "description": data.get("description", ""),
        "observed_date": data.get("observed_date"),
        "indicators": data.get("indicators", [])
    }
    mongo.db.threats.insert_one(threat)
    return jsonify({"message": "Threat data ingested successfully"}), 201

# GET /api/v1/threats/{threat_id}
def get_threat_by_id(threat_id):
    threat = mongo.db.threats.find_one({"threat_id": threat_id})  # Query by 'threat_id'
    if threat:
        threat["_id"] = str(threat["_id"])  # Convert MongoDB '_id' to string
        return jsonify(threat), 200
    return jsonify({"error": "Threat not found"}), 404


# GET /api/v1/threats
def list_threats():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    threats = mongo.db.threats.find().skip((page - 1) * per_page).limit(per_page)
    threat_list = [{"_id": str(threat["_id"]), "threat_id": threat["threat_id"], "type": threat["type"], "severity": threat["severity"]} for threat in threats]
    return jsonify(threat_list), 200


def classify_threat(threat_id):
    # Retrieve threat data from MongoDB
    threat = mongo.db.threats.find_one({"threat_id": threat_id})
    
    if threat:
        # Get both category and risk score
        category, risk_score = predict_category_and_risk(threat)
        
        # Update MongoDB with category and risk score
        mongo.db.threats.update_one(
            {"threat_id": threat_id},
            {"$set": {"classification": {"category": category, "risk_score": risk_score}}}
        )
        
        return jsonify({"threat_id": threat_id, "category": category, "risk_score": risk_score}), 200
    else:
        return jsonify({"error": "Threat not found"}), 404
    

# def generate_summary(threat_id):
#     threat = mongo.db.threats.find_one({"threat_id": threat_id})
#     if not threat:
#         return jsonify({"error": "Threat not found"}), 404

#     preprocessed_data = preprocess_for_llm(threat)
#     summary = fetch_threat_summary(preprocessed_data)

#     mongo.db.threats.update_one(
#         {"threat_id": threat_id},
#         {"$set": {"llm_summary": summary}}
#     )

#     return jsonify({"threat_id": threat_id, "summary": summary}), 200



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
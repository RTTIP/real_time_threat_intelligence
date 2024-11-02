from flask import request, jsonify
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



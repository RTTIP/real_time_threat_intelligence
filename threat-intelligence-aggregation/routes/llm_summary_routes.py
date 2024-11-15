from flask import Blueprint, jsonify
from config.db import mongo
from LLM.llm_threat_summary import fetch_threat_summary, preprocess_for_llm

summary_bp = Blueprint("summary", __name__)

@summary_bp.route('/generate_summary/<threat_id>', methods=['POST'])
def generate_summary(threat_id):
    threat = mongo.db.threats.find_one({"threat_id": threat_id})
    if not threat:
        return jsonify({"error": "Threat not found"}), 404

    preprocessed_data = preprocess_for_llm(threat)
    summary = fetch_threat_summary(preprocessed_data)

    mongo.db.threats.update_one(
        {"threat_id": threat_id},
        {"$set": {"llm_summary": summary}}
    )

    return jsonify({"threat_id": threat_id, "summary": summary}), 200

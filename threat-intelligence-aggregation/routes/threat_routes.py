from flask import Blueprint
from controllers.threat_controller import ingest_threat, get_threat_by_id, list_threats, classify_threat, predict_threat, generate_summary


threat_bp = Blueprint('threat', __name__)

#Routes for threats
threat_bp.route("/ingest", methods=["POST"])(ingest_threat)
threat_bp.route("/<threat_id>", methods=["GET"])(get_threat_by_id)
threat_bp.route("/", methods=["GET"])(list_threats)
threat_bp.route("/<threat_id>/classify", methods=["POST"])(classify_threat)
threat_bp.route("/generate_summary/<threat_id>", methods=["POST"])(generate_summary)
threat_bp.route("/predict_threat", methods=["POST"])(predict_threat)

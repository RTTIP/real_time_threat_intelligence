from flask import Blueprint, jsonify, current_app, Flask
from RITP.Models import AssetRisk

incident_bp = Blueprint("incident_bp", __name__)

def monitor_risks():
        high_risk_threshold = 90.00
        critical_assets = AssetRisk.query.filter_by(threat_level='high').all()
        for asset in critical_assets:
            risk = AssetRisk.query.filter_by(asset_id=asset.asset_id).order_by(AssetRisk.risk_id.desc()).first()
            if risk and risk.risk_score >= high_risk_threshold:
                trigger_incident_response(asset,risk)

def trigger_incident_response(asset, risk):
    print(f"Incident Triggered for {asset.asset_id} due to high risk score: {risk.risk_score}")

@incident_bp.route('/initiate_monitoring', methods=['GET'])
def initiate_monitoring():
    monitor_risks()
    return jsonify({"status": "Monitoring started"}), 200

import pandas as pd
import joblib
from flask import request, jsonify, Blueprint
from datetime import datetime
from RITP import db
from RITP.Models import Assets, AssetRisk, Incident

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/predict_impact',methods=['POST'])
def predict_impact():
    data = request.get_json()
    description = data.get('description')
    name = data.get('name')
    severity_level = data.get('severity_level')
    incident_type = data.get('incident_type')
    duration = data.get('duration')

    asset = Assets.query.filter(Assets.name.ilike(f"%{name}%")).first()
    if not asset:
        return jsonify({'error': 'Asset not found for given description'}), 404

    asset_risk = AssetRisk.query.filter_by(asset_id=asset.asset_id).first()
    if not asset_risk:
        return jsonify({'error': 'No associated asset risk found for asset'}), 404

    days_since_evaluation = (datetime.now() - asset_risk.last_evaluation).days

    features = {
        'asset_id': asset.asset_id,
        'value': asset.value,
        'criticality': asset.criticality,
        'risk_score': asset_risk.risk_score,
        'threat_level': asset_risk.threat_level,
        'days_since_evaluation': days_since_evaluation
    }

    feature_df = pd.DataFrame([features])
    feature_df = pd.get_dummies(feature_df, columns=['criticality', 'threat_level'], drop_first=True)

    model = joblib.load('C:/Users/cvnik/Desktop/impact_prediction_model.pkl')
    feature_df = feature_df.reindex(columns=model.feature_names_in_, fill_value=0)

    impact_score = model.predict(feature_df)[0]

    impact_level = "Minimal"
    if 21 <= impact_score <= 40:
        impact_level = "Low"
    elif 41 <= impact_score <= 60:
        impact_level = "Medium"
    elif 61 <= impact_score <= 80:
        impact_level = "High"
    elif 81 <= impact_score <= 100:
        impact_level = "Critical"

    new_incident = Incident(
        asset_id=asset.asset_id,
        description=description,
        impact_score=float(impact_score),
        severity_level=impact_level,
        incident_type=incident_type,
        duration=duration,
        resolved=False
    )
    db.session.add(new_incident)
    db.session.commit()

    return jsonify({
        'incident_id': new_incident.incident_id,
        'asset_id': asset.asset_id,
        'impact_score': impact_score,
        'impact_level': impact_level,
        'severity_level': severity_level,
        'incident_type': incident_type,
        'duration': duration
    })

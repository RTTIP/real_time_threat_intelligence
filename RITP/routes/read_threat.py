from decimal import Decimal
from flask import request, jsonify, Blueprint
from RITP import db
from RITP.Models import Assets, AssetRisk

threat_bp = Blueprint('threat_bp', __name__)

@threat_bp.route('/readThreat',methods=['POST'])
def readThreat():
    data = request.get_json()
    threat_desc = data.get('threat')
    assetRisk = AssetRisk.query.filter_by(risk_description=threat_desc).first()
    asset = calculateAssetRisk(assetRisk.asset_id, assetRisk.risk_description)
    return asset

def calculateAssetRisk(asset_id, risk_description):
    asset = Assets.query.get(asset_id)
    percentageIncrease = Decimal(getPercentage(risk_description))
    adjusted_value = asset.value * (1 + percentageIncrease)
    asset.value = adjusted_value
    db.session.commit()
    return jsonify({
        "assetid": asset.asset_id,
        "base_value": asset.value / (1 + percentageIncrease),
        "adjusted_value": adjusted_value
    })

def getPercentage(risk_description):
    if risk_description == 'Low':
        return 0.03
    elif risk_description == 'Medium':
        return 0.07
    else:
        return 0.12

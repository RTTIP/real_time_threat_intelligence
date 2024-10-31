import os

from datetime import datetime
from decimal import Decimal
import openai
from flask import request, jsonify

from Models import Assets, AssetRisk
from RITP import app, db

# OpenAI API key setup (set up your own key here)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/addAssets',methods=['POST'])
def addAssets():
    data =request.get_json()
    name=data.get('name')
    type=data.get('type')
    value=data.get('value',0.0)
    criticality=data.get('criticality')

    if not name or not type or criticality not in ['low', 'medium', 'high']:
        return jsonify({'error':'Did not provide complete json request'}),400

    new_asset=Assets(name=name,type=type,value=value,criticality=criticality,created_at=datetime.now(),updated_at=datetime.now())

    try:
        db.session.add(new_asset)
        db.session.commit()
        return jsonify({'success':'Assets added successfully','asset_id':new_asset.asset_id}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500

@app.route('/addAssetsRisks',methods=['POST'])
def addAssetsRisks():
    data=request.get_json()
    asset_id=data.get('asset_id')
    risk_score=data.get('risk_score')
    risk_description=data.get('risk_description')
    threat_level=data.get('threat_level')

    if not risk_score or not risk_description or threat_level not in ['low', 'medium', 'high']:
        return jsonify({'error':"Please provide correct values"}),400

    # new assets_risk can be added only to the already exisiting asset id
    assets=Assets.query.filter_by(asset_id=asset_id).first()
    if not assets:
        return jsonify({'error':'Must be assigned to a valid asset'}),500
    new_assetRisk=AssetRisk(asset_id=asset_id,risk_score=risk_score,risk_description=risk_description,threat_level=threat_level)

    try:
        db.session.add(new_assetRisk)
        db.session.commit()
        return jsonify({'success':'new asset risk has been added successfully','new_assetRisk':new_assetRisk.risk_id}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500

@app.route('/updateAsset/<int:asset_id>',methods=['PUT'])
def updateAsset(asset_id):
    data=request.get_json()
    asset=Assets.query.get(asset_id)

    if not asset:
        return jsonify({'error':'Asset not found'}),404

    for key,value in data.items():
        setattr(asset,key,value)
    db.session.commit()
    return jsonify({'success':'Asset updated succesfully'}),200

@app.route('/updateAssetRisk/<int:asset_riskId>',methods=['PUT'])
def updateAssetRisk(asset_riskId):
    data=request.get_json()
    assetRisk=AssetRisk.query.get(asset_riskId)

    if not assetRisk:
        return jsonify({'error':'Asset risk not found'}),404

    for key,value in data.items():
        setattr(assetRisk,key,value)
    db.session.commit()
    return jsonify({'success':'Asset risk updated succesfully'}),200

@app.route('/deleteAsset/<int:asset_id>',methods=['DELETE'])
def deleteAsset(asset_id):
    asset=Assets.query.get(asset_id)

    if not asset:
        return jsonify({'error':'Asset not found'}),404

    try:
        db.session.delete(asset)
        db.session.commit()
        return jsonify({'success':'Asset and associated risks deleted successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500

@app.route('/deleteAssetRisk/<int:asset_riskId>',methods=['DELETE'])
def deleteAssetRisk(asset_riskId):
    assetRisk=AssetRisk.query.get(asset_riskId)
    if not assetRisk:
        return jsonify({'error':'Asset risk not found'}),404
    try:
        db.session.delete(assetRisk)
        db.session.commit()
        return jsonify({'success':'Asset risk deleted succesfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500

@app.route('/GetAssets',methods=['GET'])
def getAssets():
    assets=Assets.query.all()
    assets_list = [
        {
            'asset_id': asset.asset_id,
            'name': asset.name,
            'type': asset.type,
            'value': asset.value,
            'criticality': asset.criticality,
            'created_at': asset.created_at,
            'updated_at': asset.updated_at
        }
        for asset in assets
    ]
    return assets_list

@app.route('/GetAssetRisks',methods=['GET'])
def getAssetRisks():
    assetRisks=AssetRisk.query.all()
    risks_list = [
        {
            "risk_id": risk.risk_id,
            "asset_id": risk.asset_id,
            "risk_score": risk.risk_score,
            "risk_description": risk.risk_description,
            "threat_level": risk.threat_level,
            "last_evaluation": risk.last_evaluation
        }
        for risk in assetRisks
    ]
    return risks_list

@app.route('/GetAssetById/<int:asset_id>',methods=['GET'])
def getAssetById(asset_id):
    asset=Assets.query.get(asset_id)
    if asset:
        # Serialize asset data to return as JSON
        asset_data = {
            'asset_id': asset.asset_id,
            'name': asset.name,
            'type': asset.type,
            'value': float(asset.value),
            'criticality': asset.criticality,
            'created_at': asset.created_at,
            'updated_at': asset.updated_at
        }
        return jsonify(asset_data), 200
    else:
        return jsonify({'error': 'Asset not found'}), 404
    return asset

@app.route('/GetAssetRiskById/<int:asset_risk_id>',methods=['GET'])
def GetAssetRiskById(asset_risk_id):
    asset_risk=AssetRisk.query.get(asset_risk_id)
    if asset_risk:
        # Return risk details as JSON
        return jsonify({
            'risk_id': asset_risk.risk_id,
            'asset_id': asset_risk.asset_id,
            'risk_score': asset_risk.risk_score,
            'risk_description': asset_risk.risk_description,
            'threat_level': asset_risk.threat_level,
            'last_evaluation': asset_risk.last_evaluation
        }), 200
    else:
        # Return a 404 error if not found
        return jsonify({'error': 'Asset risk not found'}), 404

@app.route('/readThreat',methods=['POST'])
def readThreat():
    data=request.get_json()
    threat_desc=data.get('threat')
    assetRisk=AssetRisk.query.filter_by(risk_description=threat_desc).first()
    asset=calculateAssetRisk(assetRisk.asset_id,assetRisk.risk_description)
    return asset

def calculateAssetRisk(asset_id,risk_description):
    asset=Assets.query.get(asset_id)
    percentageIncrease=Decimal(getPercentage(risk_description))
    adjusted_value=asset.value*(1+percentageIncrease)
    asset.value=adjusted_value
    db.session.commit()
    return jsonify({
        "assetid":asset.asset_id,
        "base_value":asset.value / (1 + percentageIncrease),
        "adjusted_value":adjusted_value
    })

def getPercentage(risk_description):
    if risk_description=='Low':
        return 0.03
    elif risk_description=='Medium':
        return 0.07
    else:
        return 0.12

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

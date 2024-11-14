import openai
from flask import Flask, request, jsonify, Blueprint
import os
from transformers import pipeline
from RITP.Models import Assets, AssetRisk

# Load your OpenAI API key
openai.api_key = "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"
llm_bp = Blueprint('llm', __name__)
app = Flask(__name__)


def generate_asset_report(asset):
    prompt = f"""
    Generate a detailed report for the following asset data:
    Asset Name: {asset.name}
    Asset Type: {asset.type}
    Value: ${asset.value}
    Criticality: {asset.criticality}
    Risk Score: {getattr(asset, 'risk_score', 'N/A')}
    Risk Description: {getattr(asset, 'risk_description', 'No specific risks identified')}

    Provide a summary of the asset's importance, the potential impact of any associated risks, 
    and suggest possible mitigation strategies to reduce these risks.
    """

    generator = pipeline('text-generation', model='gpt2')  # Use a free, small model like GPT-2
    response = generator(prompt, max_length=250, num_return_sequences=1)
    report = response[0]['generated_text'].strip()
    return report


@llm_bp.route('/generate_asset_report/<int:asset_id>', methods=['GET'])
def generate_asset_report_endpoint(asset_id):
    asset = Assets.query.get(asset_id)

    if not asset:
        return jsonify({"error": "Asset not found"}), 404

    # Fetch associated risk if available
    asset_risk = AssetRisk.query.filter_by(asset_id=asset_id).first()
    if asset_risk:
        asset.risk_score = asset_risk.risk_score
        asset.risk_description = asset_risk.risk_description

    report = generate_asset_report(asset)
    return jsonify({"asset_report": report})

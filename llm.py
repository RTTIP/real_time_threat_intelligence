from flask import Flask
import json
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Flask application
app = Flask(__name__)

# Check if GPU is available
device = 0 if torch.cuda.is_available() else -1

# Load the model and tokenizer
model_name = "distilgpt2"
pipe = pipeline("text-generation", model=model_name, device=device)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set the padding token to eos_token
tokenizer.pad_token = tokenizer.eos_token

# File paths
input_file_path = './CM_JSON.json'  # Input JSON file
output_file_path = './Updated_CM_JSON.json'  # Output JSON file

# Templates
crisis_template = """
Crisis Management Response:
============================
**Incident Summary**:
{incident_summary}

**Impact**:
{impact}

**Immediate Actions**:
{immediate_actions}

**Recommended Next Steps**:
{recommended_next_steps}

**Resources**:
{resources}
"""

post_incident_template = """
Post-Incident Analysis:
========================
The recent incident involves {incident_description}, affecting {affected_assets}. Immediate actions included {immediate_actions_taken}, which effectively {containment_summary}.

The recommended next steps focus on {mitigation_summary}, ensuring compliance and risk reduction. It is essential to engage with {engaged_resources} to {post_action_summary}.

**Classification**: This incident qualifies as a "{classification}". Future efforts should include {future_focus}.
========================
"""

# Functions for generating templates
def generate_communication_from_template(incident):
    incident_summary = incident.get('description', 'No description available')
    impact = f"Severity: {incident.get('severity', 'Unknown severity')}, Affected Assets: {', '.join(incident.get('affected_assets', []))}"
    immediate_actions = "Isolate affected network components, start immediate diagnostics, involve technical teams, and begin root cause analysis."
    recommended_next_steps = "Conduct thorough investigation, communicate with affected users, coordinate with cybersecurity and network teams to apply mitigation strategies."
    resources = "Cybersecurity team, network engineers, customer support for communication, incident management team."
    
    filled_template = crisis_template.format(
        incident_summary=incident_summary,
        impact=impact,
        immediate_actions=immediate_actions,
        recommended_next_steps=recommended_next_steps,
        resources=resources
    )
    
    inputs = tokenizer(filled_template, return_tensors="pt", max_length=512, truncation=True, padding=True)
    result = model.generate(
        inputs['input_ids'],
        max_length=512,
        num_return_sequences=1,
        temperature=0.7,
        do_sample=True
    )
    
    return tokenizer.decode(result[0], skip_special_tokens=True)

def generate_post_incident_analysis(incident, communication_template):
    incident_description = incident.get('description', 'an incident')
    affected_assets = ', '.join(incident.get('affected_assets', [])) or "key systems"
    immediate_actions_taken = "isolating affected systems and initiating investigative protocols"
    containment_summary = "contained the issue and limited its impact"
    mitigation_summary = "enhancing existing protocols and ensuring compliance with industry standards"
    engaged_resources = "legal and forensic resources"
    post_action_summary = "analyze and reinforce the organization's preparedness"
    classification = "Network Incident" if "network" in incident_description.lower() else "General Incident"
    future_focus = "regular system audits, incident drills, and improved employee training"

    filled_template = post_incident_template.format(
        incident_description=incident_description,
        affected_assets=affected_assets,
        immediate_actions_taken=immediate_actions_taken,
        containment_summary=containment_summary,
        mitigation_summary=mitigation_summary,
        engaged_resources=engaged_resources,
        post_action_summary=post_action_summary,
        classification=classification,
        future_focus=future_focus
    )
    
    return filled_template

# Function to process incidents
def process_incidents():
    with open(input_file_path, 'r') as f:
        incident_data = json.load(f)

    if isinstance(incident_data, dict):
        incidents = [incident_data]
    else:
        incidents = incident_data

    for incident in incidents:
        communication_template = generate_communication_from_template(incident)
        post_incident_analysis = generate_post_incident_analysis(incident, communication_template)
        incident['communication_template'] = communication_template
        incident['post-incident-response'] = post_incident_analysis

    with open(output_file_path, 'w') as f:
        json.dump(incidents, f, indent=4)

    print(f"Updated JSON saved to: {output_file_path}")
    print("\nExample of an updated incident:")
    print(json.dumps(incidents[0], indent=4))

# Flask route to execute the function
@app.route('/')
def main():
    process_incidents()
    return "JSON Processing Complete. Check the output in the terminal."

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
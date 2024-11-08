import requests

# API credentials and endpoint configuration
# waiting for other teams
API_URL = ""  
API_KEY = ""

# Crisis Communication Template
CRISIS_TEMPLATE = """
Crisis Management Response:
============================
**Incident Summary**:
{incident_summary}

**Impact**:
{impact}

**Immediate Actions**:
{immediate_actions}

**Recommended Next Steps**:
{next_steps}

**Resources**:
{resources}
============================
"""

def get_llm_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "text-davinci-003",  # Specify your model
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 150,
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response_json = response.json()
    
    # Extract LLM response text
    return response_json['choices'][0]['text'].strip()

def generate_crisis_response(incident_summary, impact):
    # Define the prompt with the initial information
    prompt = (
        f"Generate a crisis management response based on the following details:\n\n"
        f"Incident Summary: {incident_summary}\nImpact: {impact}\n\n"
        "Provide immediate actions, recommended next steps, and resources needed."
    )
    
    # Get LLM response
    llm_response = get_llm_response(prompt)
    
    # Parse LLM response into template sections (you may need custom parsing based on LLM output structure)
    immediate_actions = "Immediate actions based on the LLM output."
    next_steps = "Recommended next steps."
    resources = "Additional resources."
    
    # Format using the crisis template
    response = CRISIS_TEMPLATE.format(
        incident_summary=incident_summary,
        impact=impact,
        immediate_actions=immediate_actions,
        next_steps=next_steps,
        resources=resources
    )
    
    return response

# Example Usage
incident_summary = "A data breach was detected on the customer database."
impact = "Potential exposure of sensitive customer information."

response = generate_crisis_response(incident_summary, impact)
print(response)
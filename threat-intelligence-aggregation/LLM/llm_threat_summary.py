import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_threat_summary(threat_data):
    prompt = f"Summarize the following threat data for non-technical users:\n\n" \
             f"Threat Type: {threat_data.get('type', 'N/A')}\n" \
             f"Severity: {threat_data.get('severity', 'N/A')}\n" \
             f"Description: {threat_data.get('description', 'N/A')}\n" \
             f"Indicators: {', '.join(threat_data.get('indicators', []))}\n\n" \
             "Explain the impact and recommended actions in simple terms."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def preprocess_for_llm(threat_data):
    return {
        "type": threat_data.get("type", "Unknown"),
        "severity": threat_data.get("severity", "Unknown"),
        "description": threat_data.get("description", ""),
        "indicators": threat_data.get("indicators", [])
    }

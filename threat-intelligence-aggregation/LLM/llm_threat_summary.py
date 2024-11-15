import openai
import os

openai.api_key = "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"

def fetch_threat_summary(threat_data):
    # Define the system prompt and user prompt for chat completion
    system_message = "You are an assistant helping summarize threat data for non-technical users."
    user_prompt = f"Summarize the following threat data:\n\n" \
                  f"Threat Type: {threat_data.get('type', 'N/A')}\n" \
                  f"Severity: {threat_data.get('severity', 'N/A')}\n" \
                  f"Description: {threat_data.get('description', 'N/A')}\n" \
                  f"Indicators: {', '.join(threat_data.get('indicators', []))}\n\n" \
                  "Explain the impact and recommended actions in simple terms."

    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def preprocess_for_llm(threat_data):
    return {
        "type": threat_data.get("type", "Unknown"),
        "severity": threat_data.get("severity", "Unknown"),
        "description": threat_data.get("description", ""),
        "indicators": threat_data.get("indicators", [])
    }

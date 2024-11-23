# from transformers import pipeline
# import logging

# logging.basicConfig(level=logging.INFO)

# # Load the summarization model
# summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


# def fetch_threat_summary(threat_data):
#     logging.info(f"Input threat data: {threat_data}")

#     # Construct the input text from threat data
#     input_text = (
#         f"A cybersecurity threat has been identified:\n"
#         f"Type: {threat_data.get('type', 'Unknown')}\n"
#         f"Severity: {threat_data.get('severity', 'Unknown')}\n"
#         f"Description: {threat_data.get('description', 'No description available')}\n"
#         f"Indicators: {', '.join(threat_data.get('indicators', [])).strip() or 'None'}.\n\n"
#         f"Please summarize this information for non-technical users, including potential impact and recommended actions."
#     )
#     # Generate the summary
#     try:
#         summary = summarizer(input_text, max_length=250, min_length=120, do_sample=True, top_k=50, temperature=0.9)
#         logging.info(f"Generated summary: {summary[0]['summary_text']}")
#         return summary[0]['summary_text']
#     except Exception as e:
#         return f"Error generating summary: {str(e)}"


# def preprocess_for_llm(threat_data):
#     return {
#         "type": threat_data.get("type", "Unknown"),
#         "severity": threat_data.get("severity", "Unknown"),
#         "description": threat_data.get("description", ""),
#         "indicators": threat_data.get("indicators", [])
#     }

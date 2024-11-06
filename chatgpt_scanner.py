import openai

class SecurityRiskScanner:
    def __init__(self, api_key):
        """
        Initialize the SecurityRiskScanner with the OpenAI API key.
        """
        self.api_key = api_key
        openai.api_key = self.api_key

    def scan_code(self, input_code):
        """
        Analyze the given input code for security risks and potential threats using the OpenAI API.
        
        Args:
        - input_code (str): The code to be scanned.
        
        Returns:
        - dict: A dictionary with detected security risks and their potential threats.
        """
        prompt = (
            "You are a security expert. Analyze the following code for potential security risks and threats. "
            "Provide detailed explanations of any identified vulnerabilities, their possible impact, and "
            "recommendations to mitigate these risks:\n\n"
            f"{input_code}\n"
        )
        messages = [{"role":"system","content":"You are a security expert. Analyze code for potential security risks and threats."},{"role":"user","content":f"Analyze the following code:\n\n{input_code}"}]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Specify the model to use
                messages=messages,
                max_tokens=1500,  # Adjust as needed
                temperature=0.7
		)
            return self._parse_response(response)

        except Exception as e:
            return {"error": str(e)}

    def _parse_response(self, response):
    	"""
    	Parse the response from the OpenAI API (ChatCompletion).
    	"""
    	print("Raw response:", response)  # Debugging line to see the raw response
    	if response and "choices" in response:
    	    analysis = response["choices"][0].get("message", {}).get("content", "").strip()
    	    if analysis:
    	        return {"analysis": analysis}
    	return {"error": "No valid response or empty content received from API."}



# Example usage
if __name__ == "__main__":
    # Replace 'your_openai_api_key' with your actual API key
    scanner = SecurityRiskScanner(api_key="your_openai_api_key")
    code_to_scan = "import os\n\n def insecure_function(user_input):\n	os.system(f'echo {user_input}')"
    result = scanner.scan_code(code_to_scan)
    print(result)
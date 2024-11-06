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
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # Adjust the engine if needed
                prompt=prompt,
                max_tokens=1500,  # You can adjust this as per your requirements
                temperature=0.7
            )
            return self._parse_response(response)

        except Exception as e:
            return {"error": str(e)}

    def _parse_response(self, response):
        """
        Parse the response from the OpenAI API.
        
        Args:
        - response (openai.Completion): The response object from OpenAI API.
        
        Returns:
        - dict: A dictionary containing the formatted response.
        """
        if response and "choices" in response:
            analysis = response["choices"][0].get("text", "").strip()
            return {"analysis": analysis}
        return {"error": "No valid response received from API."}


# Example usage
if __name__ == "__main__":
    # Replace 'your_openai_api_key' with your actual API key
    scanner = SecurityRiskScanner(api_key="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")
    code_to_scan = "
    import os

    def insecure_function(user_input):
        os.system(f'echo {user_input}')
    "
    result = scanner.scan_code(code_to_scan)
    print(result)
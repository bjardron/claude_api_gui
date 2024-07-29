import requests

class ClaudeAPI:
    def __init__(self, api_key):
        # Initialize the API with the provided key and base URL
        self.api_key = api_key
        self.base_url = "https://api.claude.com/v1"

    def send_message(self, system_prompt, model, temperature, max_tokens, message):
        # Set up the headers and data for the API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": system_prompt + "\n\n" + message,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        # Send the request to the Claude API
        response = requests.post(f"{self.base_url}/messages", headers=headers, json=data)
        response.raise_for_status()
        # Return the response text from Claude
        return response.json()["choices"][0]["text"]

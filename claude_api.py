import requests
import logging

logging.basicConfig(level=logging.DEBUG)

class ClaudeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"

    def send_message(self, system_prompt, model, temperature, max_tokens, message):
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        
        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        logging.debug(f"Sending request to {self.base_url}/messages with headers {headers} and data {data}")
        
        response = requests.post(f"{self.base_url}/messages", headers=headers, json=data)
        logging.debug(f"Response status code: {response.status_code}")
        logging.debug(f"Response content: {response.content}")
        
        response.raise_for_status()
        
        return response.json()["content"][0]["text"]

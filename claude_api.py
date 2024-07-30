import anthropic
from config import API_KEY

class ClaudeAPI:
    def __init__(self):
        self.api_key = API_KEY
        if not self.api_key:
            raise ValueError("API key not found. Please set the API_KEY in config.py.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def send_message(self, system_prompt, model, temperature, max_tokens, message):
        if not message.strip():
            return "Message content is empty, skipping..."
        
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            return self.format_response(response)
        except anthropic.APIStatusError as e:
            print(f"API Status Error: {e.status_code} - {e.message}")
            return f"Error: {e.status_code} - {e.message}"
        except Exception as e:
            print(f"Error occurred: {e}")
            return f"Error: {e}"

    def format_response(self, response):
        return response.content[0].text

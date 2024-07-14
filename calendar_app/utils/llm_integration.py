import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm_guidance(calendar_json, user_query):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("No API key found. Please set the OPENAI_API_KEY environment variable in the .env file.")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides guidance based on a user's calendar. The calendar data will be provided in JSON format."
            },
            {
                "role": "user",
                "content": f"Here is my calendar data: {calendar_json}\n\nBased on this, {user_query}"
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
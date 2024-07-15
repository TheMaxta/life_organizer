from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import json
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm_guidance(user_input, current_calendar):
    prompt = f"""
    Given the following calendar and user input, suggest updates to the calendar in JSON format.
    Current calendar:
    {json.dumps(current_calendar, indent=2)}

    User input: {user_input}

    Provide a JSON response with the following structure:
    {{
        "actions": [
            {{
                "operation": "add" or "update" or "delete",
                "name": "Action name",
                "description": "Action description",
                "start_time": "HH:MM",
                "end_time": "HH:MM",
                "type": "RoutineAction" or "UncommonAction",
                "days": [0,1,2,3,4,5,6] (for RoutineAction, where 0 is Monday),
                "frequency": "DAILY" or "WEEKLY" or "MONTHLY" or "YEARLY" (for RoutineAction),
                "date": "YYYY-MM-DD" (for UncommonAction)
            }}
        ]
    }}
    """

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that translates natural language calendar updates into JSON format."},
        {"role": "user", "content": prompt}
    ])

    try:
        suggested_updates = json.loads(response.choices[0].message.content)
        return suggested_updates
    except json.JSONDecodeError:
        return {"error": "Failed to parse LLM response"}


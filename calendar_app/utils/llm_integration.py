import os
from openai import OpenAI
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    IMPORTANT RULES:
    1. ALL fields must be filled for each action, even if you have to make reasonable assumptions.
    2. For RoutineActions, ALWAYS specify both 'days' and 'frequency'.
    3. For UncommonActions, ALWAYS specify 'date'.
    4. If the user doesn't specify a time, use common sense to suggest appropriate times.
    5. If the user doesn't specify duration, assume 1 hour by default.
    6. If the user doesn't specify frequency for a routine action, assume WEEKLY.
    7. If the user doesn't specify days for a routine action, assume [0,1,2,3,4] (weekdays).
    8. If the type isn't clear from the user input, prefer RoutineAction for recurring events and UncommonAction for one-time events.
    9. Always provide a brief but informative description.
    10. If updating or deleting, assume it's for the most recent or upcoming instance of that action if not specified.

    Remember, your role is to interpret the user's intent and fill in any missing details with reasonable assumptions.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates natural language calendar updates into JSON format. You always provide all required fields, making reasonable assumptions when necessary."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        suggested_updates = json.loads(response.choices[0].message.content)
        return validate_and_fill_updates(suggested_updates)
    except json.JSONDecodeError:
        return {"error": "Failed to parse LLM response"}

def validate_and_fill_updates(suggested_updates):
    for action in suggested_updates.get('actions', []):
        if action['type'] == 'RoutineAction':
            action['days'] = action.get('days', [0,1,2,3,4])
            action['frequency'] = action.get('frequency', 'WEEKLY')
        elif action['type'] == 'UncommonAction':
            if 'date' not in action:
                action['date'] = datetime.now().strftime('%Y-%m-%d')
        
        if 'start_time' not in action:
            action['start_time'] = '09:00'
        if 'end_time' not in action:
            start = datetime.strptime(action['start_time'], '%H:%M')
            end = (start + timedelta(hours=1)).strftime('%H:%M')
            action['end_time'] = end
        
        action['description'] = action.get('description', f"No description provided for {action['name']}")

    return suggested_updates
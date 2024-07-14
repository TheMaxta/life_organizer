import json
from datetime import datetime

class Calendar:
    def __init__(self):
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def get_actions_for_date(self, date):
        return [action for action in self.actions if action.occurs_on(date)]

    def to_json(self):
        return json.dumps({
            "actions": [
                {
                    "name": action.name,
                    "description": action.description,
                    "duration": action.duration,
                    "type": action.__class__.__name__,
                    "days": action.days if hasattr(action, 'days') else None,
                    "frequency": action.frequency.name if hasattr(action, 'frequency') else None,
                    "date": action.date.isoformat() if hasattr(action, 'date') else None
                }
                for action in self.actions
            ]
        })
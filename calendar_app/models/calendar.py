# calendar_app/models/calendar.py

import json
from calendar_app.database import Session, ActionDB
from calendar_app.models.actions import RoutineAction, UncommonAction, Frequency
from datetime import datetime, time

class Calendar:
    def __init__(self):
        self.session = Session()

    def to_json(self):
        actions = self.get_all_actions()
        return json.dumps({
            "actions": [
                {
                    "name": action.name,
                    "description": action.description,
                    "start_time": action.start_time.strftime("%H:%M") if isinstance(action.start_time, time) else None,
                    "end_time": action.end_time.strftime("%H:%M") if isinstance(action.end_time, time) else None,
                    "type": action.type,
                    "days": action.days.split(',') if action.days else None,
                    "frequency": action.frequency.name if action.frequency else None,
                    "date": action.date.isoformat() if action.date else None
                }
                for action in actions
            ]
        })

    def from_json(self, json_data):
        data = json.loads(json_data)
        for action_data in data['actions']:
            if action_data['type'] == 'RoutineAction':
                action = RoutineAction(
                    action_data['name'],
                    action_data['description'],
                    datetime.strptime(action_data['start_time'], "%H:%M").time(),
                    datetime.strptime(action_data['end_time'], "%H:%M").time(),
                    list(map(int, action_data['days'])),
                    Frequency[action_data['frequency']]
                )
            elif action_data['type'] == 'UncommonAction':
                action = UncommonAction(
                    action_data['name'],
                    action_data['description'],
                    datetime.strptime(action_data['start_time'], "%H:%M").time(),
                    datetime.strptime(action_data['end_time'], "%H:%M").time(),
                    datetime.fromisoformat(action_data['date']).date()
                )
            self.add_action(action)
    def add_action(self, action):
        action_db = ActionDB(
            name=action.name,
            description=action.description,
            start_time=action.start_time,
            end_time=action.end_time,
            type=action.__class__.__name__,
            days=','.join(map(str, action.days)) if hasattr(action, 'days') else None,
            frequency=action.frequency if hasattr(action, 'frequency') else None,
            date=action.date if hasattr(action, 'date') else None
        )
        self.session.add(action_db)
        self.session.commit()

    def get_actions_for_date(self, date):
        actions = []
        for action_db in self.session.query(ActionDB).all():
            if action_db.type == 'RoutineAction':
                action = RoutineAction(
                    action_db.name,
                    action_db.description,
                    action_db.start_time,
                    action_db.end_time,
                    list(map(int, action_db.days.split(','))),
                    action_db.frequency
                )
                if action.occurs_on(date):
                    actions.append(action)
            elif action_db.type == 'UncommonAction':
                action = UncommonAction(
                    action_db.name,
                    action_db.description,
                    action_db.start_time,
                    action_db.end_time,
                    action_db.date
                )
                if action.occurs_on(date):
                    actions.append(action)
        return actions

    def get_all_actions(self):
        return self.session.query(ActionDB).all()

    def close(self):
        self.session.close()
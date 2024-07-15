# Calendar App Database Operations Guide

## Overview
This guide covers basic operations for the SQLite database used in our Calendar App. The database is managed using SQLAlchemy ORM.

## Database Structure
Our main table is `actions`, represented by the `ActionDB` class in `database.py`.

## Basic Operations

### 1. Querying Actions

To get all actions:

```python
def get_all_actions(self):
    return self.session.query(ActionDB).all()
```
To filter actions:
```python
def get_actions_by_name(self, name):
    return self.session.query(ActionDB).filter(ActionDB.name == name).all()
```
2. Adding a New Action

```python

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

```
3. Updating an Action
```python
def update_action(self, action_id, **kwargs):
    action = self.session.query(ActionDB).get(action_id)
    for key, value in kwargs.items():
        setattr(action, key, value)
    self.session.commit()

```
4. Deleting an Action

```python
def delete_action(self, action_id):
    action = self.session.query(ActionDB).get(action_id)
    self.session.delete(action)
    self.session.commit()

```

Advanced Operations
1. Querying Actions for a Specific Date Range

```python

from sqlalchemy import and_

def get_actions_in_date_range(self, start_date, end_date):
    return self.session.query(ActionDB).filter(
        and_(ActionDB.date >= start_date, ActionDB.date <= end_date)
    ).all()

```

2. Querying Actions by Frequency
```python
def get_actions_by_frequency(self, frequency):
    return self.session.query(ActionDB).filter(ActionDB.frequency == frequency).all()

```
Error Handling
Always wrap database operations in try-except blocks:
```python
from sqlalchemy.exc import SQLAlchemyError

try:
    # Perform database operation
    self.session.commit()
except SQLAlchemyError as e:
    self.session.rollback()
    print(f"An error occurred: {str(e)}")

```
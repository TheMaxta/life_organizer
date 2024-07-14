from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum

class Frequency(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4

class BaseAction(ABC):
    def __init__(self, name, description, start_time, end_time):
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time

    def calculate_duration(self):
        # Create datetime objects for today with the given start and end times
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)
        
        # If end_time is earlier than start_time, assume it's on the next day
        if end_datetime <= start_datetime:
            end_datetime += timedelta(days=1)
        
        # Calculate the duration
        duration = end_datetime - start_datetime
        
        return duration

    def get_duration_string(self):
        duration = self.calculate_duration()
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60
        return f"{hours} hours, {minutes} minutes"
    
    @abstractmethod
    def occurs_on(self, date):
        pass

class RoutineAction(BaseAction):
    def __init__(self, name, description, start_time, end_time, days, frequency):
        super().__init__(name, description, start_time, end_time)
        self.days = days
        self.frequency = frequency

    def occurs_on(self, date):
        if self.frequency == Frequency.DAILY:
            return True
        elif self.frequency == Frequency.WEEKLY:
            return date.weekday() in self.days
        elif self.frequency == Frequency.MONTHLY:
            return date.day in self.days
        elif self.frequency == Frequency.YEARLY:
            return (date.month, date.day) in self.days
        return False

class UncommonAction(BaseAction):
    def __init__(self, name, description, start_time, end_time, date):
        super().__init__(name, description, start_time, end_time)
        self.date = date

    def occurs_on(self, date):
        return date == self.date
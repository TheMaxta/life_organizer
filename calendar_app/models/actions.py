from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

class Frequency(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4

class BaseAction(ABC):
    def __init__(self, name, description, duration):
        self.name = name
        self.description = description
        self.duration = duration

    @abstractmethod
    def occurs_on(self, date):
        pass

class RoutineAction(BaseAction):
    def __init__(self, name, description, duration, days, frequency):
        super().__init__(name, description, duration)
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
    def __init__(self, name, description, duration, date):
        super().__init__(name, description, duration)
        self.date = date

    def occurs_on(self, date):
        return date == self.date
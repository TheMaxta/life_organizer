import unittest
from datetime import datetime
from models.actions import RoutineAction, UncommonAction, Frequency

class TestActions(unittest.TestCase):
    def test_routine_action(self):
        action = RoutineAction("Test", "Description", 30, [0, 1], Frequency.WEEKLY)
        self.assertTrue(action.occurs_on(datetime(2023, 7, 10)))  # A Monday
        self.assertTrue(action.occurs_on(datetime(2023, 7, 11)))  # A Tuesday
        self.assertFalse(action.occurs_on(datetime(2023, 7, 12)))  # A Wednesday

    def test_uncommon_action(self):
        action = UncommonAction("Test", "Description", 60, datetime(2023, 7, 15))
        self.assertTrue(action.occurs_on(datetime(2023, 7, 15)))
        self.assertFalse(action.occurs_on(datetime(2023, 7, 16)))

if __name__ == '__main__':
    unittest.main()
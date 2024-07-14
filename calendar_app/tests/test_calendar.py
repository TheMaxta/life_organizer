import unittest
from datetime import datetime
from models.calendar import Calendar
from models.actions import RoutineAction, UncommonAction, Frequency

class TestCalendar(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar()

    def test_add_action(self):
        action = RoutineAction("Test", "Description", 30, [0, 1], Frequency.WEEKLY)
        self.calendar.add_action(action)
        self.assertEqual(len(self.calendar.actions), 1)

    def test_get_actions_for_date(self):
        routine_action = RoutineAction("Routine", "Description", 30, [0, 1], Frequency.WEEKLY)
        uncommon_action = UncommonAction("Uncommon", "Description", 60, datetime(2023, 7, 15))
        self.calendar.add_action(routine_action)
        self.calendar.add_action(uncommon_action)

        monday_actions = self.calendar.get_actions_for_date(datetime(2023, 7, 10))  # A Monday
        self.assertEqual(len(monday_actions), 1)
        self.assertEqual(monday_actions[0].name, "Routine")

        saturday_actions = self.calendar.get_actions_for_date(datetime(2023, 7, 15))  # A Saturday
        self.assertEqual(len(saturday_actions), 1)
        self.assertEqual(saturday_actions[0].name, "Uncommon")

    def test_to_json(self):
        action = RoutineAction("Test", "Description", 30, [0, 1], Frequency.WEEKLY)
        self.calendar.add_action(action)
        json_data = self.calendar.to_json()
        self.assertIn("Test", json_data)
        self.assertIn("WEEKLY", json_data)

if __name__ == '__main__':
    unittest.main()
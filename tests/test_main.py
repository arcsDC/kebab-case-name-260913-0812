import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import EventManager, load_config

class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.config = load_config()
        self.manager = EventManager(self.config)

    def test_create_event(self):
        guild_id = 12345
        user_id = 67890
        event_id = self.manager.create_event(guild_id, user_id, "Test Event", "2023-12-25T10:00:00")
        self.assertIsNotNone(event_id)
        event = self.manager.get_event(guild_id, event_id)
        self.assertEqual(event["title"], "Test Event")
        self.assertEqual(event["organizer_id"], user_id)
        self.assertEqual(len(event["attendees"]), 0)

    def test_join_event(self):
        guild_id = 12345
        user_id = 67890
        event_id = self.manager.create_event(guild_id, user_id, "Test Event", "2023-12-25T10:00:00")
        
        attendee_id = 11111
        success = self.manager.join_event(guild_id, event_id, attendee_id)
        self.assertTrue(success)
        
        event = self.manager.get_event(guild_id, event_id)
        self.assertIn(attendee_id, event["attendees"])

    def test_leave_event(self):
        guild_id = 12345
        user_id = 67890
        event_id = self.manager.create_event(guild_id, user_id, "Test Event", "2023-12-25T10:00:00")
        
        attendee_id = 11111
        self.manager.join_event(guild_id, event_id, attendee_id)
        
        success = self.manager.leave_event(guild_id, event_id, attendee_id)
        self.assertTrue(success)
        
        event = self.manager.get_event(guild_id, event_id)
        self.assertNotIn(attendee_id, event["attendees"])

    def test_join_nonexistent_event(self):
        guild_id = 12345
        event_id = "nonexistent"
        attendee_id = 11111
        success = self.manager.join_event(guild_id, event_id, attendee_id)
        self.assertFalse(success)

    def test_leave_nonexistent_event(self):
        guild_id = 12345
        event_id = "nonexistent"
        attendee_id = 11111
        success = self.manager.leave_event(guild_id, event_id, attendee_id)
        self.assertFalse(success)

    def test_get_event_status(self):
        guild_id = 12345
        user_id = 67890
        event_id = self.manager.create_event(guild_id, user_id, "Test Event", "2023-12-25T10:00:00")
        
        self.manager.join_event(guild_id, event_id, 11111)
        self.manager.join_event(guild_id, event_id, 22222)
        
        status = self.manager.get_event_status(guild_id, event_id)
        self.assertEqual(status["total_attendees"], 2)
        self.assertEqual(status["event_id"], event_id)

if __name__ == '__main__':
    unittest.main()

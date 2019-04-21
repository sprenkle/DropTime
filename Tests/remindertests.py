from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock
import unittest
from reminder import Reminder
from ledcontroller import LedController


class TestReminder(unittest.TestCase):

    def test_when_no_reminders_calls_clear_reminder_on_led_controller(self):
        print("dd")
        now = datetime.now() - timedelta(days=1)
        now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.000')
        reminder_list = [{'display': [0, 255, 0, 255, 0, 255], 'tagid': 314, 'start': now_str, 'duration': 300}]
        device_id = "device_id"
        led_device = Mock()
        tag_repo = LedController(led_device)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()

        reminder = Reminder(tag_repo, None, led_controller)
        reminder.update()
        led_controller.clear_reminder.assert_called_once()

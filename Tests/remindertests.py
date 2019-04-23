from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock
import unittest
from reminder import Reminder
from ledcontroller import LedController


class TestReminder(unittest.TestCase):

    def test_when_no_reminders_calls_clear_reminder_on_led_controller(self):
        reminder_list = []
        led_device = Mock()
        tag_repo = LedController(led_device)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()

        reminder = Reminder(tag_repo, None, led_controller)
        reminder.update()
        led_controller.clear_reminder.assert_called_once()

    def test_when_one_reminder_before_now_calls_clear_reminder(self):
        now = datetime.now() - timedelta(seconds=400)
        now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.000')
        reminder_list = [{'display': [0, 255, 0, 255, 0, 255], 'tagid': 314, 'start': now_str, 'duration': 300}]
        led_device = Mock()
        tag_repo = LedController(led_device)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()

        reminder = Reminder(tag_repo, None, led_controller)
        reminder.update()
        led_controller.clear_reminder.assert_called_once()

    def test_when_one_reminder_after_now_calls_clear_reminder(self):
        now = datetime.now() + timedelta(seconds=400)
        now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.000')
        reminder_list = [{'display': [0, 255, 0, 255, 0, 255], 'tagid': 314, 'start': now_str, 'duration': 300}]
        led_device = Mock()
        tag_repo = LedController(led_device)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()

        reminder = Reminder(tag_repo, None, led_controller)
        reminder.update()
        led_controller.clear_reminder.assert_called_once()

    def test_when_one_reminder_during_now_calls_set_reminder(self):
        now = datetime.now()
        now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.000')
        reminder_list = [{'display': [[0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]], 'tagid': 314,
                          'start': now_str, 'duration': 300}]
        led_device = Mock()
        tag_repo = LedController(led_device)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()

        reminder = Reminder(tag_repo, None, led_controller)
        reminder.update()
        led_controller.set_reminder.assert_called_once_with([[0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                                                             [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                                                             [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                                                             [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                                                             [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                                                             [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]])

    def test_when_one_reminder_but_tag_found_calls_clear_reminder(self):
        now = datetime.now()
        now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.000')
        reminder_list = [{'display': [[0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]], 'tagid': 314,
                          'start': now_str, 'duration': 300}]
        led_device = Mock()
        tag_repo = LedController(led_device)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()

        reminder = Reminder(tag_repo, None, led_controller)
        reminder.process_reminders(314)
        reminder.update()
        led_controller.clear_reminder.assert_called_once()
        #led_controller.

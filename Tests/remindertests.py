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
        reminder_list = [{'display': '[0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]', 'tagid': 314, 'start': now_str, 'duration': 300}]
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
        reminder_list = [{'display': '[0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]', 'tagid': 314, 'start': now_str, 'duration': 300}]
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
        reminder_list = [{'display': '[0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]', 'tagid': 314,
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
        reminder_list = [{'display': '[0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]', 'tagid': 314,
                          'start': now_str, 'duration': 300}]
        led_device = Mock()
        tag_repo = LedController(led_device)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()

        reminder = Reminder(tag_repo, None, led_controller)
        reminder.process_reminders(314)
        reminder.update()
        led_controller.clear_reminder.assert_called_once()

    def test_when_two_reminder_but_tag_found_calls_does_not_clear_reminder(self):
        now = datetime.now()
        now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.000')
        reminder_list = [
            {'display': '[255, 255, 255], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]', 'tagid': 314,
             'start': now_str, 'duration': 300}, {'display': '[255, 0, 255], [0, 255, 0], [0, 255, 0], [0, 255, 0],'
                                                             ' [0, 255, 0]', 'tagid': 316,
                                                             'start': now_str, 'duration': 300}]
        led_device = Mock()
        tag_repo = LedController(led_device)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()

        reminder = Reminder(tag_repo, None, led_controller)
        reminder.process_reminders(314)
        reminder.update()
        led_controller.clear_reminder.assert_not_called()
        led_controller.set_reminder.assert_called_once_with([[0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                                                             [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                                                             [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                                                             [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                                                             [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                                                             [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]])

    def test_when_two_reminder_two_tag_found_calls_clear_reminder(self):
        now = datetime.now()
        now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.000')
        reminder_list = [
            {'display': '[255, 255, 255], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]', 'tagid': 314,
             'start': now_str, 'duration': 300}, {'display': '[255, 0, 255], [0, 255, 0], [0, 255, 0], [0, 255, 0],'
                                                             ' [0, 255, 0]', 'tagid': 316,
                                                  'start': now_str, 'duration': 300}]
        led_device = Mock()
        tag_repo = LedController(led_device)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()

        reminder = Reminder(tag_repo, None, led_controller)
        reminder.process_reminders(314)
        reminder.process_reminders(316)
        reminder.update()
        led_controller.clear_reminder.assert_called_once()

#test = {'tagid': '1110945734', 'display': '[255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255]', 'deviceid': '08f98cd6-3602-41ee-aa27-a6768412254e', 'reminderid': 'c40d96c0-cd5b-4d63-978d-a90c548c4fc6', 'userid': '72be6ab4-727b-4257-ba1d-ef58a3349bfc', 'start': '2019-04-02T15:39:20.000', 'duration': 43200, 'showled': 1, 'sunday': 1, 'monday': 1, 'tuesday': 1, 'wednesday': 1, 'thursday': 1, 'friday': 1, 'saturday': 1}
from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock
import unittest
from reminder import Reminder
from ledcontroller import LedController


class TestReminder(unittest.TestCase):

    def test_execute(self):
        from tagrepository import TagRepository
        from configuration import Configuration

        configuration = Configuration("..\configuration.json")
        tag_repo = TagRepository(configuration)

        led_controller = Mock()

        reminder = Reminder(tag_repo, "08f98cd6-3602-41ee-aa27-a6768412254e", led_controller)
        reminder.update()


    def test_when_no_reminders_calls_clear_reminder_on_led_controller(self):
        from tagrepository import TagRepository
        from configuration import Configuration

        reminder_list = {"reminders": []}
        configuration = Configuration("..\configuration.json")
        tag_repo = TagRepository(configuration)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()

        reminder = Reminder(tag_repo, None, led_controller)
        reminder.update()
        led_controller.clear_reminder.assert_called_once()

    def test_when_one_reminder_before_now_has_tag_calls_clear_reminder(self):
        from tagrepository import TagRepository
        from configuration import Configuration
        now = datetime.now() - timedelta(seconds=400)
        now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.000')
        reminder_list = {
                "reminders": [
                    {
                        "reminderid": "fa663d5b-217a-4365-ad27-635851868b45",
                        "name": "Reminder1",
                        "userid": "72be6ab4-727b-4257-ba1d-ef58a3349bfc",
                        "deviceid": "08f98cd6-3602-41ee-aa27-a6768412254e",
                        "start": now_str,
                        "duration": 36000,
                        "showled": 1,
                        "sunday": 1,
                        "monday": 1,
                        "tuesday": 1,
                        "wednesday": 1,
                        "thursday": 1,
                        "friday": 1,
                        "saturday": 1
                    }
                ]
            }
        configuration = Configuration("..\configuration.json")
        tag_repo = TagRepository(configuration)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()
        reminder = Reminder(tag_repo, "08f98cd6-3602-41ee-aa27-a6768412254e", led_controller)
        reminder.update()
        reminder.execute("3172271240")
        reminder.update()
        led_controller.clear_reminder.assert_called_once()

    def test_when_one_reminder_before_now_no_tag_calls_set_reminder(self):
        from tagrepository import TagRepository
        from configuration import Configuration
        now = datetime.now() - timedelta(seconds=400)
        now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.000')
        reminder_list = {
                "reminders": [
                    {
                        "reminderid": "fa663d5b-217a-4365-ad27-635851868b45",
                        "name": "Reminder1",
                        "userid": "72be6ab4-727b-4257-ba1d-ef58a3349bfc",
                        "deviceid": "08f98cd6-3602-41ee-aa27-a6768412254e",
                        "start": now_str,
                        "duration": 36000,
                        "showled": 1,
                        "sunday": 1,
                        "monday": 1,
                        "tuesday": 1,
                        "wednesday": 1,
                        "thursday": 1,
                        "friday": 1,
                        "saturday": 1
                    }
                ]
            }
        configuration = Configuration("..\configuration.json")
        tag_repo = TagRepository(configuration)
        tag_repo.get_reminders = MagicMock(return_value=reminder_list)
        led_controller = Mock()
        reminder = Reminder(tag_repo, "08f98cd6-3602-41ee-aa27-a6768412254e", led_controller)
        reminder.update()
        led_controller.set_reminder.assert_called_once()




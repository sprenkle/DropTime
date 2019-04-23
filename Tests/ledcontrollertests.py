from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock
import unittest
from reminder import Reminder
from ledcontroller import LedController


class TestLedController(unittest.TestCase):

    def test_set_reminder_will_show_leds_when_show_is_called(self):
        led_device = Mock()
        led_controller = LedController(led_device)
        led_controller.set_reminder([[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]])
        led_controller.show()
        led_device.show.assert_called_once_with([[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]])






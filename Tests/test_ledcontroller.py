from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock
import unittest
from reminder import Reminder
from ledcontroller import LedController


class TestLedController(unittest.TestCase):

    def test_when_set_unknown_tag_it_calls_show_unknown_tag(self):
        device = Mock()
        controller = LedController(device)
        controller.set_unknown_tag()
        controller.show()
        device.show.assert_called_once()
        device.show.assert_called_with([[0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255],
                              [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0],
                              [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255],
                              [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0],
                              [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0]])

    def test_when_set_have_tracking_tag_it_calls_show_tracking_display(self):
        device = Mock()
        controller = LedController(device)
        controller.set_have_tracking_tag()
        controller.show()
        controller.show()
        self.assertEqual(device.show.call_count, 2)
        device.show.assert_called_with([[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255]])

    def test_when_no_tag_outputs_zeros(self):
        device = Mock()
        controller = LedController(device)
        controller.show()
        device.show.assert_called_with([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def test_when_tacking_tag_set_then_cleared_will_show_zero(self):
        device = Mock()
        controller = LedController(device)
        controller.set_have_tracking_tag()
        controller.clear_tag()
        controller.show()
        device.show.assert_called_with([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def test_when_progress_tag_set_then_cleared_will_show_zero(self):
        device = Mock()
        controller = LedController(device)
        controller.set_progress(60, 30)
        controller.clear_tag()
        controller.show()
        device.show.assert_called_with([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])

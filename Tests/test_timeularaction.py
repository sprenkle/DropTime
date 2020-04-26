import unittest
from unittest.mock import MagicMock, Mock
from timeularaction import TimeularAction


class TimularActionTests(unittest.TestCase):

    def test_no_progress_tracking_new_tag_from_null_calls_led_controller_set_have_tracking_tag_and_calls_timeular(self):
        tag_id = 123
        identifier = 214
        user_id = 34
        api_key = "api_key"
        api_secret = "api_secret"
        token = "token"

        api = Mock()
        api.get_token.return_value = token

        tag_repo = Mock()
        tag_repo.contains_id.return_value = True
        tag_repo.tags_to_actions.return_value = {"identifier": identifier, "userid": user_id}
        tag_repo.get_activity.return_value = {"show": 0,  "dailyGoals": 1, "dailytimeSec": 60}
        tag_repo.get_api_key_token.return_value = (api_key, api_secret)

        led_controller = Mock()

        action = TimeularAction(api, tag_repo, led_controller, "123")
        action.execute(tag_id)
        led_controller.set_have_tracking_tag.assert_called_once()
        api.start_tracking.assert_called_once()

    def test_unknown_tag_from_null_calls_led_controller_set_unknown_tag_and_does_not_call_timeular(self):
        tag_id = 123
        identifier = 214
        user_id = 34
        api_key = "api_key"
        api_secret = "api_secret"
        token = "token"

        api = Mock()
        api.get_token.return_value = token

        tag_repo = Mock()
        tag_repo.contains_id.return_value = False
        tag_repo.tags_to_actions.return_value = {"identifier": identifier, "userid": user_id}
        tag_repo.get_activity.return_value = {"show": 1,  "dailyGoals": 1, "dailytimeSec": 60}
        tag_repo.get_api_key_token.return_value = (api_key, api_secret)

        led_controller = Mock()

        action = TimeularAction(api, tag_repo, led_controller, "123")
        action.execute(tag_id)
        led_controller.set_unknown_tag()
        api.start_tracking.assert_not_called()

    def test_with_progress_tracking_new_tag_from_null_calls_led_controller_set_have_tracking_tag_and_calls_timeular(self):
        tag_id = 123
        identifier = 214
        user_id = 34
        api_key = "api_key"
        api_secret = "api_secret"
        token = "token"

        api = Mock()
        api.get_token.return_value = token

        tag_repo = Mock()
        tag_repo.contains_id.return_value = True
        tag_repo.tags_to_actions.return_value = {"identifier": identifier, "userid": user_id}
        tag_repo.get_activity.return_value = {"show": 1,  "dailyGoals": 1, "dailytimeSec": 60}
        tag_repo.get_api_key_token.return_value = (api_key, api_secret)
        tag_repo.get_activity_duration.return_value = 30

        led_controller = Mock()

        action = TimeularAction(api, tag_repo, led_controller, "123")
        action.execute(tag_id)

        led_controller.set_have_tracking_tag.assert_not_called()
        led_controller.set_unknown_tag.assert_not_called()
        led_controller.set_progress.assert_called_once()
        led_controller.set_progress.assert_called_with(60, 0)
        api.start_tracking.assert_called_once()

    def test_with_progress_tracking_new_tag_then_removed_calls_clear_tag(self):
        tag_id = 123
        identifier = 214
        user_id = 34
        api_key = "api_key"
        api_secret = "api_secret"
        token = "token"

        api = Mock()
        api.get_token.return_value = token

        tag_repo = Mock()
        tag_repo.contains_id.return_value = True
        tag_repo.tags_to_actions.return_value = {"identifier": identifier, "userid": user_id}
        tag_repo.get_activity.return_value = {"show": 1,  "dailyGoals": 2, "dailytimeSec": 60}
        tag_repo.get_api_key_token.return_value = (api_key, api_secret)
        tag_repo.get_activity_duration.return_value = 30

        led_controller = Mock()

        action = TimeularAction(api, tag_repo, led_controller, "123")
        action.execute(tag_id)
        action.execute(None)

        led_controller.set_have_tracking_tag.assert_not_called()
        led_controller.set_unknown_tag.assert_not_called()
        led_controller.set_progress.assert_called_once()
        led_controller.set_progress.assert_called_with(60, 30)
        led_controller.clear_tag.assert_called_once()
        api.start_tracking.assert_called_once()
        api.stop_tracking.assert_called_once()

    def test_calling_with_new_tagid_calls_start(self):
        tag_id = 123
        identifier = 214
        user_id = 34
        api_key = "api_key"
        api_secret = "api_secret"
        token = "token"

        api = Mock()
        api.get_token.return_value = token

        tag_repo = Mock()
        tag_repo.contains_id.return_value = True
        tag_repo.tags_to_actions.return_value = {"identifier": identifier, "userid": user_id}
        tag_repo.get_activity.return_value = {"show": 1, "dailyGoals": 2, "dailytimeSec": 60}
        tag_repo.get_api_key_token.return_value = (api_key, api_secret)
        tag_repo.get_activity_duration.return_value = 30

        #time_spent = self.tag_repository.get_activity_duration(1, tag_to_action["identifier"], self.start_time, now)

        led_controller = Mock()

        action = TimeularAction(api, tag_repo, led_controller, "123")
        action.execute(tag_id)
        action.execute(tag_id)

        led_controller.set_have_tracking_tag.assert_not_called()
        led_controller.set_unknown_tag.assert_not_called()
        led_controller.set_progress.assert_called_with(60, 30)
        api.start_tracking.assert_called_once()
        api.stop_tracking.assert_not_called()

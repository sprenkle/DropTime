import unittest
import mock
from droptime import DropTime


class TestDropTime(unittest.TestCase):

    @mock.patch('ledcontroller.LedController')
    @mock.patch('configuration.Configuration')
    @mock.patch('tagrepository.TagRepository')
    @mock.patch('mockrfireader.MockRfiReader')
    @mock.patch('actions.Actions')
    @mock.patch('logger.Logger')
    def test_initial_tag_detection_does_not_call_tag_logging(self, led_controller, configuration,
                                                             tag_repository, tag_reader, actions, logger):
        configuration.get_value.return_value = 'device_id'
        droptime = DropTime(led_controller, configuration, tag_repository, tag_reader, actions, logger)
        droptime.process_actions(314)
        tag_repository.log_tag.assert_not_called()

    @mock.patch('ledcontroller.LedController')
    @mock.patch('configuration.Configuration')
    @mock.patch('tagrepository.TagRepository')
    @mock.patch('mockrfireader.MockRfiReader')
    @mock.patch('actions.Actions')
    @mock.patch('logger.Logger')
    def test_call_tag_logging_when_last_tag_not_null_and_current_tag_null(self, led_controller, configuration,
                                                                          tag_repository, tag_reader, actions, logger):
        configuration.get_value.return_value = 'device_id'
        droptime = DropTime(led_controller, configuration, tag_repository, tag_reader, actions, logger)
        droptime.process_actions(314)
        droptime.process_actions(None)
        tag_repository.log_tag.assert_called_once_with(314, 'device_id', mock.ANY, mock.ANY)

    @mock.patch('ledcontroller.LedController')
    @mock.patch('configuration.Configuration')
    @mock.patch('tagrepository.TagRepository')
    @mock.patch('mockrfireader.MockRfiReader')
    @mock.patch('actions.Actions')
    @mock.patch('logger.Logger')
    def test_call_tag_logging_when_last_tag_not_null_and_current_tag__not_null(self, led_controller,
                                                                               configuration, tag_repository,
                                                                               tag_reader, actions, logger):
        configuration.get_value.return_value = 'device_id'
        droptime = DropTime(led_controller, configuration, tag_repository, tag_reader, actions, logger)
        droptime.process_actions(314)
        droptime.process_actions(412)
        tag_repository.log_tag.assert_called_once_with(314, 'device_id', mock.ANY, mock.ANY)


if __name__ == '__main__':
    unittest.main()

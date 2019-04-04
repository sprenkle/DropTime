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
        tag_reader.read_card.return_value = 314
        droptime = DropTime(led_controller, configuration, tag_repository, tag_reader, actions, logger)
        droptime.process_actions()
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
        tag_reader.read_card.return_value = 314
        droptime = DropTime(led_controller, configuration, tag_repository, tag_reader, actions, logger)
        droptime.process_actions()
        tag_reader.read_card.return_value = None
        droptime.process_actions()
        droptime.process_actions()
        droptime.process_actions()

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
        tag_reader.read_card.return_value = 314
        # led_controller, configuration, tag_repository, tag_reader, all_actions, my_logger
        droptime = DropTime(led_controller, configuration, tag_repository, tag_reader, actions, logger)
        droptime.process_actions()

        tag_reader.read_card.return_value = 412
        droptime.process_actions()
        droptime.process_actions()
        droptime.process_actions()
        tag_repository.log_tag.assert_called_once_with(314, 'device_id', mock.ANY, mock.ANY)

    @mock.patch('ledcontroller.LedController')
    @mock.patch('configuration.Configuration')
    @mock.patch('tagrepository.TagRepository')
    @mock.patch('mockrfireader.MockRfiReader')
    @mock.patch('actions.Actions')
    @mock.patch('logger.Logger')
    def test_turning_on_show_non_result_display_and_off(self, led_controller, configuration, tag_repository,
                                                                               tag_reader, actions, logger):
        configuration.get_value.return_value = 'device_id'
        tag_reader.read_card.return_value = 314
        # led_controller, configuration, tag_repository, tag_reader, all_actions, my_logger
        droptime = DropTime(led_controller, configuration, tag_repository, tag_reader, actions, logger)
        droptime.process_actions()

        tag_reader.read_card.return_value = 412
        droptime.process_actions()
        tag_repository.log_tag.assert_called_once_with(314, 'device_id', mock.ANY, mock.ANY)
        led_controller.show_non_result_display.called_once()

        tag_reader.read_card.return_value = None
        droptime.process_actions()
        droptime.process_actions()
        droptime.process_actions()
        led_controller.clear.called_once()

    @mock.patch('ledcontroller.LedController')
    @mock.patch('configuration.Configuration')
    @mock.patch('tagrepository.TagRepository')
    @mock.patch('mockrfireader.MockRfiReader')
    @mock.patch('actions.Actions')
    @mock.patch('logger.Logger')
    def test_turning_show_non_action_tag(self, led_controller, configuration, tag_repository,
                                                                               tag_reader, actions, logger):
        configuration.get_value.return_value = 'device_id'
        tag_reader.read_card.return_value = 314
        # led_controller, configuration, tag_repository, tag_reader, all_actions, my_logger
        droptime = DropTime(led_controller, configuration, tag_repository, tag_reader, actions, logger)
        droptime.process_actions()

        tag_reader.read_card.return_value = 412
        droptime.process_actions()
        tag_repository.log_tag.assert_called_once_with(314, 'device_id', mock.ANY, mock.ANY)
        led_controller.show_non_result_display.called_once()

        tag_reader.read_card.return_value = None
        droptime.process_actions()
        droptime.process_actions()
        droptime.process_actions()
        led_controller.clear.called_once()




if __name__ == '__main__':
    unittest.main()

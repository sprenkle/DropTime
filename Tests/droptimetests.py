import unittest
import mock
from droptime import DropTime


class TestDropTime(unittest.TestCase):

    @mock.patch('tagrepository.TagRepository')
    @mock.patch('mockrfireader.MockRfiReader')
    @mock.patch('actions.Actions')
    @mock.patch('logger.Logger')
    def test_initial_tag_detection_does_not_call_tag_logging(self, tag_repository, tag_reader, actions, logger):
        tag_reader.read_card.return_value = 314

        droptime = DropTime(tag_repository, tag_reader, actions, logger)
        droptime.process_actions()

        tag_repository.log_tag.assert_not_called()

    @mock.patch('tagrepository.TagRepository')
    @mock.patch('mockrfireader.MockRfiReader')
    @mock.patch('actions.Actions')
    @mock.patch('logger.Logger')
    def test_call_tag_logging_when_last_tag_not_null_and_current_tag_null(self, tag_repository, tag_reader, actions, logger):
        tag_reader.read_card.return_value = 314
        droptime = DropTime(tag_repository, tag_reader, actions, logger)
        droptime.process_actions()

        tag_reader.read_card.return_value = None
        droptime.process_actions()
        droptime.process_actions()
        droptime.process_actions()

        tag_repository.log_tag.assert_called_once_with(314, mock.ANY, mock.ANY)


    @mock.patch('tagrepository.TagRepository')
    @mock.patch('mockrfireader.MockRfiReader')
    @mock.patch('actions.Actions')
    @mock.patch('logger.Logger')
    def test_call_tag_logging_when_last_tag_not_null_and_current_tag__not_null(self, tag_repository, tag_reader, actions, logger):
        tag_reader.read_card.return_value = 314
        droptime = DropTime(tag_repository, tag_reader, actions, logger)
        droptime.process_actions()

        tag_reader.read_card.return_value = 412
        droptime.process_actions()
        droptime.process_actions()
        droptime.process_actions()
        tag_repository.log_tag.assert_called_once_with(314, mock.ANY, mock.ANY)


if __name__ == '__main__':
    unittest.main()
import unittest
import mock
from timeularaction import TimeularAction


class TestDropTime(unittest.TestCase):
    pass
    # @mock.patch('timeularapi.TimularApi')
    # @mock.patch('tagrepository.TagRepository')
    # def test_initial_tag_detection_does_not_call_tag_logging(self, api, tag_repository):
    #     tag_id = "123"
    #     action = TimeularAction(api, tag_repository, logger)
    #     result = action.execute(tag_id)


if __name__ == '__main__':
    unittest.main()

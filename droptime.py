import time
import datetime
import sys
from actions import Actions
from timeularaction import TimeularAction
from configuration import Configuration
from mockledcontroller import MockLedController


class DropTime:

    def __init__(self, tag_repository, tag_reader, all_actions, my_logger):
        self.reader = tag_reader
        self.last_read = None
        self.actions = all_actions
        self.mlogger = my_logger
        self.none_count = 0
        self.tag_repository = tag_repository
        self.tag_start = None

    def run(self):
        self.mlogger.log("started run")
        while True:
            self.process_actions()
            time.sleep(.1)

    def process_actions(self):
        card_id = self.reader.read_card()
        if card_id is None:
            self.none_count = self.none_count + 1
        if card_id is not None:
            self.none_count = 0
        if self.last_read != card_id and (card_id is not None or self.none_count > 2):
            # we had a last read so we must log the stop time of the tag
            if self.last_read is not None:
                self.log_tag(self.last_read, self.tag_start, datetime.datetime.utcnow())

            # The tag_id is not null so we must give a start time
            if card_id is not None:
                self.tag_start = datetime.datetime.utcnow()

            self.mlogger.log("run - new id " + str(card_id))
            self.last_read = card_id
            self.actions.execute(card_id)
            self.none_count = 0

    def log_tag(self, tag_id, start, end):
        self.tag_repository.log_tag(tag_id, start, end)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        from mockrfireader import MockRfiReader
        # from mockapi import MockApi
        from timeularapi import TimularApi
        from debuglogger import DebugLogger
        from mockleddevice import MockLedDevice
        from tagrepository import TagRepository

        leddevice = MockLedDevice()
        logger = DebugLogger()
        reader = MockRfiReader()
        # api = MockApi()
        configuration = Configuration("debug_config.json")
        tag_repository = TagRepository(configuration)
        api = TimularApi(configuration, tag_repository, logger)
    else:
        from rfireader import RfiReader
        from timeularapi import TimularApi
        from debuglogger import DebugLogger
        #from leddevice import LedDevice
        from mockleddevice import MockLedDevice
        from tagrepository import TagRepository

        leddevice = MockLedDevice()
        logger = DebugLogger()
        reader = RfiReader()
        configuration = Configuration("configuration.json")
        tag_repository = TagRepository(configuration)

        api = TimularApi(configuration, tag_repository, logger)

    actions = Actions(tag_repository, MockLedController(leddevice), logger, TimeularAction(api, tag_repository, logger))
    dropTime = DropTime(tag_repository, reader, actions, logger)
    dropTime.run()



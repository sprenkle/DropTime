import time
import sys
from actions import Actions
from timeularaction import TimeularAction
from tagrepository import TagRepository
from configuration import Configuration
from ledcontroller import LedController


class DropTime:

    def __init__(self, tag_reader, all_actions, my_logger):
        self.reader = tag_reader
        self.last_read = None
        self.actions = all_actions
        self.mlogger = my_logger
        self.none_count = 0

    def run(self):
        self.mlogger.log("started run")
        while True:
            card_id = self.reader.read_card()
            if card_id is None:
                self.none_count = self.none_count + 1
            if card_id is not None:
                self.none_count = 0
            if self.last_read != card_id and (card_id is not None or self.none_count > 2):
                self.mlogger.log("run - new id " + str(card_id))
                self.last_read = card_id
                self.actions.execute(card_id)
                self.none_count = 0
            time.sleep(.1)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        from mockrfireader import MockRfiReader
        # from mockapi import MockApi
        from timeularapi import TimularApi
        from debuglogger import DebugLogger
        from mockleddevice import MockLedDevice

        leddevice = MockLedDevice()
        logger = DebugLogger()
        reader = MockRfiReader()
        # api = MockApi()
        configuration = Configuration("debug_config.json")
        tagRepository = TagRepository(configuration)
        api = TimularApi(configuration, tagRepository, logger)
    else:
        from rfireader import RfiReader
        from timeularapi import TimularApi
        from debuglogger import DebugLogger
        #from leddevice import LedDevice
        from mockleddevice import MockLedDevice

        leddevice = MockLedDevice()
        logger = DebugLogger()
        reader = RfiReader()
        configuration = Configuration("configuration.json")
        tagRepository = TagRepository(configuration)

        api = TimularApi(configuration, tagRepository, logger)

    actions = Actions(LedController(leddevice), logger, TimeularAction(api, tagRepository))
    dropTime = DropTime(reader, actions, logger)
    dropTime.run()



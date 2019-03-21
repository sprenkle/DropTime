import time
import sys
from actions import Actions
from timeularaction import TimeularAction
from cardrepository import CardRepository


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
        from mockapi import MockApi
        from debuglogger import DebugLogger
        logger = DebugLogger()
        reader = MockRfiReader()
        api = MockApi()
    else:
        from rfireader import RfiReader
        from timeularapi import TimularApi
        from debuglogger import DebugLogger
        logger = DebugLogger()
        reader = RfiReader()
        api = TimularApi("NDcwMDBfYzU5MTUwMDQ2OWU4NDA4OWExZjFlMTZlNDhlNjFlMDM=",
                   "NDJkNDY1MjZhMDk5NDAyZTg2YjNkNWIyNDVmYmFiYjc=", logger)

    actions = Actions(logger, TimeularAction(api, CardRepository()))
    dropTime = DropTime(reader, actions, logger)
    dropTime.run()



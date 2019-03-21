import time
import sys
from actions import Actions
from timeularaction import TimeularAction
from stopaction import StopAction


class DropTime:

    def __init__(self, tag_reader, all_actions, my_logger):
        self.reader = tag_reader
        self.last_read = None
        self.actions = all_actions
        self.mlogger = my_logger

    def run(self):
        self.mlogger.log("started run")
        while True:
            card_id = self.reader.read_card()
            self.mlogger.log("read " + str(card_id))
            if self.last_read != card_id:
                self.mlogger.log("run new id " + str(card_id))
                self.last_read = card_id
                self.actions.execute(card_id)
            time.sleep(1)


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
                   "NDJkNDY1MjZhMDk5NDAyZTg2YjNkNWIyNDVmYmFiYjc=")

    actions = Actions(logger, TimeularAction(api))
    dropTime = DropTime(reader, actions, logger)
    dropTime.run()



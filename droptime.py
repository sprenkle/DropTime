from timeularapi import TimularApi
from mockrfireader import MockRfiReader
from actions import Actions
import time


class DropTime:

    def __init__(self, timeular_api, reader, actions):
        self.api = timeular_api
        self.reader = reader
        self.last_read = None
        self.actions = actions

    def run(self):
        while True:
            card_id = self.reader.read_card()
            if card_id is not None:
                if self.last_read != card_id:
                    self.last_read = card_id
                    self.actions.execute(card_id)
            time.sleep(.1)


if __name__ == "__main__":
    api = TimularApi("NDcwMDBfYzU5MTUwMDQ2OWU4NDA4OWExZjFlMTZlNDhlNjFlMDM=",
                     "NDJkNDY1MjZhMDk5NDAyZTg2YjNkNWIyNDVmYmFiYjc=")
    reader = MockRfiReader()
    actions = Actions()
    dropTime = DropTime(api, reader, actions)
    dropTime.run()



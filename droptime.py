from rfireader import RfiReader
from actions import Actions
import time


class DropTime:

    def __init__(self, tag_reader, all_actions):
        self.reader = tag_reader
        self.last_read = None
        self.actions = all_actions

    def run(self):
        while True:
            card_id = self.reader.read_card()
            if self.last_read != card_id:
                self.last_read = card_id
                self.actions.execute(card_id)
            time.sleep(.1)


if __name__ == "__main__":
    reader = RfiReader()
    actions = Actions()
    dropTime = DropTime(reader, actions)
    dropTime.run()



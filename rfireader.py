import RPi.GPIO as GPIO
from Read import Reader


class RfiReader:
    # arr = array.array('i', [1, 2, 3])
    def __init__(self):
        self.reader = Reader()

    def read_card(self):
        tag_id = self.reader.read_id_no_block()
        if tag_id is not None and tag_id == 474735937816:
            GPIO.cleanup()
            quit()
        return tag_id


    def read_card_block(self):
        tag_id = self.reader.read_id_no_block()
        print(tag_id)
        GPIO.cleanup()


if __name__ == "__main__":
    reader = RfiReader()
    reader.read_card_block()

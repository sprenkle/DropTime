import RPi.GPIO as GPIO
import SimpleMFRC522


class RfiReader:
    # arr = array.array('i', [1, 2, 3])
    def __init__(self):
        self.reader = SimpleMFRC522.SimpleMFRC522()

    def read_card(self):
        tag_id, text = self.reader.read_id_no_block()
        if tag_id is not None and tag_id == 474735937816:
            GPIO.cleanup()
            quit()
        return tag_id

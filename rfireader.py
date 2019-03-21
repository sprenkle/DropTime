import RPi.GPIO as GPIO
import SimpleMFRC522


class RfiReader:
    # arr = array.array('i', [1, 2, 3])
    def __init__(self):
        GPIO.cleanup()
        self.reader = SimpleMFRC522.SimpleMFRC522()

    def __del__(self):
        GPIO.cleanup()

    def read_card(self):
        tag_id, text = self.reader.read()
        if tag_id == "474735937816":
            GPIO.cleanup()
            quit()
        return tag_id

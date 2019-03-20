import RPi.GPIO as GPIO
import SimpleMFRC522

class RfiReader:
    # arr = array.array('i', [1, 2, 3])
    def __init__(self):
        self.reader = SimpleMFRC522.SimpleMFRC522()

    def __del__(self):
        GPIO.cleanup

    def read_card(self):
        id, text = self.reader.read()
        return str(id)

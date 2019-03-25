import RPi.GPIO as GPIO

class StopAction:

    def __init__(self):
        pass

    def execute(self, tag_id):
        if tag_id == "474735937816":
            GPIO.cleanup()
            quit()

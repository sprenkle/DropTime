import RPi.GPIO as GPIO

class StopAction:

    def __init__(self):
        pass

    def is_actionable(self, tag_id):
        return tag_id == "474735937816"

    def execute(self, tag_id):
        GPIO.cleanup()
        quit()

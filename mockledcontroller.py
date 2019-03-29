class MockLedController:

    def __init__(self):
        pass

    def have_reminder(self):
        return False

    def start_progress(self, goal_time, start_amount):
        pass

    def stop_progress(self):
        pass

    # This takes a reminder_id and a array of 6 sets of ints that
    # will turn the lights on
    def set_reminder(self, reminder_id, leds):
        pass

    def remove_reminder(self, reminder_id):
        pass

    def show(self):
        pass

    def show_progress(self):
        pass

    def show_reminder(self):
        pass
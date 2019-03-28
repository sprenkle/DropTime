import datetime

class LedController:

    def __init__(self, led_device):
        self.reminder_dict = dict()
        self.led_device = led_device
        self.deleting_showing = False
        self.progress_active = False
        self.progress_goal_time_sec = 0
        self.progress_start_amount_time_sec = 0
        self.progress_started_time = None

    def start_progress(self, goal_time, start_amount):
        self.progress_active = True
        self.progress_started_time = datetime.datetime.utcnow()

    def stop_progress(self):
        self.progress_active = False

    # This takes a reminder_id and a array of 6 sets of ints that
    # will turn the lights on
    def set_reminder(self, reminder_id, leds):
        self.reminder_dict[reminder_id] = leds

    def remove_reminder(self, reminder_id):
        if reminder_id in self.reminder_dict:
            del self.reminder_dict[reminder_id]
        if len(self.reminder_dict) == 0:
            self.deleting_showing = True

    def show(self):
        key_list = list(self.reminder_dict.keys())
        if len(key_list) == 0:
            if self.deleting_showing:
                self.led_device.show([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                      [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                      [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                      [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                      [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
                self.deleting_showing = False
                return
        led_array = [];
        index = 0
        for i in range(4):
            s = self.reminder_dict[key_list[index]]
            for j in range(6):
                led_array.append(s[j])
            index += 1
            if index >= len(key_list):
                index = 0
        self.led_device.show(led_array)

    def show_progress(self):
        pass

    def show_reminder(self):
        pass

if __name__ == "__main__":
    from leddevice import LedDevice

    led_controller = LedController(LedDevice())
    led_controller.set_reminder(1, [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]])
    led_controller.set_reminder(2, [[4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6]])
    led_controller.show()
    led_controller.remove_reminder(1)
    led_controller.show()
    led_controller.remove_reminder(2)
    led_controller.show()


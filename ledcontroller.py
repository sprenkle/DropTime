import datetime
import math
import sys


class LedController:

    def __init__(self, led_device):
        self.reminder_dict = dict()
        self.led_device = led_device
        self.deleting_showing = False
        self.progress_active = False
        self.progress_goal_time_sec = 0
        self.progress_start_amount_time_sec = 0
        self.progress_started_time = None

    def have_reminder(self):
        return len(self.reminder_dict.keys()) > 0

    def start_progress(self, goal_time, start_amount):
        self.progress_active = True
        self.progress_started_time = datetime.datetime.utcnow()
        self.progress_goal_time_sec = goal_time
        self.progress_start_amount_time_sec = start_amount

    def stop_progress(self):
        self.progress_active = False
        self.deleting_showing = True

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
        if self.deleting_showing:
            self.led_device.show([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
            self.deleting_showing = False
            self.progress_active = False

        if self.have_reminder():
            self.show_reminder()
        else:
            if self.progress_active:
                self.show_progress()

    def show_progress(self):
        if not isinstance(self.progress_goal_time_sec, int):  # todo fix this
            return
        total_time = self.progress_start_amount_time_sec + \
                     (datetime.datetime.utcnow() - self.progress_started_time).seconds
        percent = total_time / int(self.progress_goal_time_sec)
        result_over = 0
        if percent <= 1:
            result_under = math.floor(percent * 24)
            if result_under < 1:
                result_under = 1
        else:
            result_under = 24

        if 1 < percent:
            if percent <= 2:
                result_over = math.floor((percent - 1) * 24)
            else:
                result_over = 24
        led_array = []
        index = 0;
        for i in range(result_under):
            led_array.append([0, 255, 0])
            index += 1
        for i in range(24 - index):
            led_array.append([0, 0, 0])
            index += 1
        for i in range(result_over):
            led_array[i] = [255, 0, 0]
        if result_over == 24:
            for i in range(12):
                led_array[i * 2] = [0, 255, 0]

        self.led_device.show(led_array)

    def show_reminder(self):
        key_list = list(self.reminder_dict.keys())
        if len(key_list) == 0:
            return
        led_array = []
        index = 0
        for i in range(4):
            s = self.reminder_dict[key_list[index]]
            for j in range(6):
                led_array.append(s[j])
            index += 1
            if index >= len(key_list):
                index = 0
        self.led_device.show(led_array)

    def clear(self):
        self.led_device.show([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def show_non_result_display(self):
        self.led_device.show([[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255]])

    def show_non_action_tag(self):
        self.led_device.show([[0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255],
                              [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0],
                              [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255],
                              [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0],
                              [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0]])


if __name__ == "__main__":
    import time

    if len(sys.argv) == 2 and sys.argv[1] == "test":
        from mockleddevice import MockLedDevice
        led_device = MockLedDevice()
    else:
        from leddevice import LedDevice
        led_device = LedDevice()

    led_controller = LedController(led_device)
    delay = .1

    led_controller.start_progress(5, 0)
    for i in range(120):
        led_controller.show()
        time.sleep(delay)
    led_controller.set_reminder(1, [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]])
    led_controller.set_reminder(2, [[4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6]])
    led_controller.show()
    # time.sleep(delay)
    # led_controller.remove_reminder(1)
    # led_controller.show()
    # time.sleep(delay)
    # led_controller.remove_reminder(2)
    # led_controller.show()
    # led_controller.show_non_result_display()

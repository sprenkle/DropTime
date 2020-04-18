import datetime
import math
import sys
import logging


class LedController:

    def __init__(self, led_device):
        self.led_device = led_device
        self.reminder_leds = None
        self.progress_goal_time_sec = 0
        self.progress_start_amount_time_sec = 0
        self.progress_started_time = datetime.datetime.now()
        self.tracking_progress = False
        self.__have_unknown_tag = False
        self.__have_tracking_tag = False

    def set_unknown_tag(self):
        self.__have_unknown_tag = True

    def set_have_tracking_tag(self):
        self.__have_tracking_tag = True

    def clear_tag(self):
        self.__have_unknown_tag = False
        self.__have_tracking_tag = False
        self.tracking_progress = False

    def set_reminder(self, leds):
        self.reminder_leds = leds

    def clear_reminder(self):
        self.reminder_leds = None

    def set_progress(self, goal_time, previous_time):
        logging.info("set_progress with goal_time={} previous_time={}".format(goal_time, previous_time))
        self.progress_goal_time_sec = goal_time
        self.progress_start_amount_time_sec = previous_time
        self.progress_started_time = datetime.datetime.utcnow()
        self.tracking_progress = True

    def show(self):
        if self.reminder_leds is not None:
            self.led_device.show(self.reminder_leds)
            return

        if self.tracking_progress:
            self.show_progress()
            return

        if self.__have_tracking_tag:
            self.show_tracking_display()
            return

        if self.__have_unknown_tag:
            self.show_unknown_tag()
            return

        self.led_device.show([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def show_progress(self):
        time_diff = (datetime.datetime.utcnow() - self.progress_started_time).seconds
        total_time = self.progress_start_amount_time_sec + time_diff
        percent = total_time / float(self.progress_goal_time_sec)
        logging.info("now={} started_time={}  total_time={} goal_time={} Led percent = {} ".
                     format(datetime.datetime.utcnow(), self.progress_started_time, total_time,
                            float(self.progress_goal_time_sec), percent))
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
        index = 0
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
        if led_array[0] == 0:
            led_array[0] = [0, 255, 0]

        self.led_device.show(led_array)

    def show_led(self, led_array):
        self.led_device.show(led_array)

    def clear(self):
        self.led_device.show([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def show_tracking_display(self):
        self.led_device.show([[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                              [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255]])

    def show_tracking_api_error_display(self):
        self.led_device.show([[0, 0, 255], [0, 0, 255], [255, 0, 0], [0, 0, 255], [0, 0, 255],
                              [255, 0, 0], [0, 0, 255], [0, 0, 255], [255, 0, 0], [0, 0, 255],
                              [0, 0, 255], [255, 0, 0], [0, 0, 255], [0, 0, 255], [255, 0, 0],
                              [0, 0, 255], [0, 0, 255], [255, 0, 0], [0, 0, 255], [0, 0, 255],
                              [255, 0, 0], [0, 0, 255], [0, 0, 255], [255, 0, 0]])



    def show_unknown_tag(self):
        self.led_device.show([[0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255],
                              [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0],
                              [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255],
                              [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0],
                              [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0]])


if __name__ == "__main__":
    import time
    from configuration import Configuration

    if len(sys.argv) == 2 and sys.argv[1] == "test":
        from mockleddevice import MockLedDevice
        led_device = MockLedDevice()
    else:
        file = "configuration.json"
        from leddevice import LedDevice
        led_device = LedDevice(Configuration(file))

    led_controller = LedController(led_device)
    delay = .1

    # led_controller.start_progress(5, 0)
    # for i in range(120):
    #     led_controller.show()
    #     time.sleep(delay)
    # led_controller.set_reminder(1, [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]])
    # led_controller.set_reminder(2, [[4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6]])
    # led_controller.show()
    # led_controller.clear()
    # time.sleep(delay)
    # led_controller.remove_reminder(1)
    # led_controller.show()
    # time.sleep(delay)
    # led_controller.remove_reminder(2)
    # led_controller.show()
    # led_controller.show_non_result_display()
    led_controller.show_tracking_display()
    led_controller.show()
    time.sleep(15)
    led_controller.clear_tag()
    led_controller.show()

import time
import datetime
import sys
from actions import Actions
from timeularaction import TimeularAction
from configuration import Configuration
import logging
from reminder import Reminder


class DropTime:

    def __init__(self, led_controller,  configuration, tag_repository, tag_reader, all_actions, reminder):
        self.reader = tag_reader
        self.last_read = None
        self.actions = all_actions
        self.none_count = 0
        self.tag_repository = tag_repository
        self.tag_start = None
        self.configuration = configuration
        self.device_id = self.configuration.get_value("device", "device_id")
        self.led_controller = led_controller
        self.reminder = reminder
        self.has_reminder = False

    def run(self):
        logging.debug("started run")
        while True:
            try:
                card_id = self.reader.read_card()
                logging.debug("card_id read is {}".format(card_id))
                self.reminder.update()
                self.process_actions(card_id)
                self.process_reminders(card_id)
                self.led_controller.show()
            except Exception as e:
                print(e)
                time.sleep(10)
            time.sleep(.1)

    def process_reminders(self, card_id):
        self.reminder.have_tag(card_id)
        reminder_led_list = self.reminder.get_display()
        if len(reminder_led_list) == 0:
            if self.has_reminder:
                self.led_controller.clear()
            self.has_reminder = False
            return
        self.has_reminder = True
        led_display = []
        index = 0
        for i in range(4):
            for j in range(6):
                value = eval(reminder_led_list[index])[j]
                led_display.append(value)
            index = i % len(reminder_led_list)
        self.led_controller.set_reminder(led_display)

    def have_reminders(self):
        return False

    def process_results(self, result_list):
        for result in result_list:
            if result is not None and "has_progress" in result:
                if result["has_progress"]:
                    print(result["has_progress"])
                    goal_time = result["goal_time"]
                    start_amount = result["total_amount_time"]
                    self.led_controller.start_progress(goal_time, start_amount)
                    return False  # not showing result, led will show blue
                else:
                    self.led_controller.stop_progress()
                return True  # not showing result, led will show blue
        return False # not showing result, led will show blue

    def process_actions(self, card_id):
        if card_id is None:
            self.none_count = self.none_count + 1
        if card_id is not None:
            self.none_count = 0

        if self.last_read != card_id and (card_id is not None or self.none_count > 2):
            logging.info("Tag changed tag_id={}".format(card_id))
            # we had a last read so we must log the stop time of the tag
            if self.last_read is not None:
                self.log_tag(self.last_read, self.tag_start, datetime.datetime.utcnow())

            # The tag_id is not null so we must give a start time
            if card_id is not None:
                self.tag_start = datetime.datetime.utcnow()

            logging.info("run - new id " + str(card_id))
            self.last_read = card_id

            action_result_list = self.actions.execute(card_id)
            action_result = action_result_list["ActionReturnType"]

            # determine how to display the led
            if self.reminder.has_reminders():
                self.process_reminders()
            else:
                if card_id is None:
                    self.led_controller.stop_progress()
                    self.led_controller.clear()
                    logging.info("returned Result list = {}".format(action_result))
                elif action_result == "NoDisplay":
                    self.led_controller.show_non_result_display()
                elif action_result == "Unidentified":
                    self.led_controller.show_non_action_tag()
                elif action_result == "Progress":
                    goal_time = action_result_list["goal_total"]
                    total_time = action_result_list["time_spent"]
                    self.led_controller.start_progress(goal_time, total_time)

            logging.debug("Exiting process_actions")

    def show_blue(self):
        self.led_controller.show_non_result_display()

    def log_tag(self, tag_id, start, end):
        self.tag_repository.log_tag(tag_id, self.device_id, start, end)


if __name__ == "__main__":
    from ledcontroller import LedController

    if len(sys.argv) == 2 and sys.argv[1] == "test":
        from nanorfiled import NanoRfiLed
        from timeularapi import TimularApi
        from tagrepository import TagRepository
        nano = NanoRfiLed()
        led_device = nano
        reader = nano
        configuration = Configuration("debug_config.json")
        tag_repository = TagRepository(configuration)
        api = TimularApi(configuration, tag_repository)
    else:
        from rfireader import RfiReader
        from timeularapi import TimularApi
        from leddevice import LedDevice
        from tagrepository import TagRepository
        configuration = Configuration("configuration.json")
        led_device = LedDevice(configuration)
        reader = RfiReader()
        tag_repository = TagRepository(configuration)
        api = TimularApi(configuration, tag_repository)

    device_id = configuration.get_value("device", "device_id")
    actions = Actions(TimeularAction(api, tag_repository))
    dropTime = DropTime(LedController(led_device), configuration, tag_repository, reader, actions, Reminder(tag_repository, device_id))
    dropTime.run()



import time
import datetime
import sys
from actions import Actions
from timeularaction import TimeularAction
from configuration import Configuration
from mockledcontroller import MockLedController


class DropTime:

    def __init__(self, led_controller,  configuration, tag_repository, tag_reader, all_actions, my_logger):
        self.reader = tag_reader
        self.last_read = None
        self.actions = all_actions
        self.logger = my_logger
        self.none_count = 0
        self.tag_repository = tag_repository
        self.tag_start = None
        self.configuration = configuration
        self.device_id = self.configuration.get_value("device", "device_id")
        self.led_controller = led_controller

    def run(self):
        self.logger.log("started run")
        while True:
            self.process_actions()
            self.led_controller.show();
            time.sleep(.1)

    def process_reminders(self):
        pass

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

    def process_actions(self):
        card_id = self.reader.read_card()
        self.logger.log("card_id read is {}".format(card_id))
        if card_id is None:
            self.none_count = self.none_count + 1
        if card_id is not None:
            self.none_count = 0

        if self.last_read != card_id and (card_id is not None or self.none_count > 2):
            self.logger.log("Tag changed tag_id={}".format(card_id))
            # we had a last read so we must log the stop time of the tag
            if self.last_read is not None:
                self.log_tag(self.last_read, self.tag_start, datetime.datetime.utcnow())

            # The tag_id is not null so we must give a start time
            if card_id is not None:
                self.tag_start = datetime.datetime.utcnow()
                self.led_controller.stop_progress()

            self.logger.log("run - new id " + str(card_id))
            self.last_read = card_id

            action_result_list = self.actions.execute(card_id)
            action_result = action_result_list["ActionReturnType"]

            # determine how to display the led
            if self.have_reminders():
                self.process_reminders()
            else:
                if card_id is None:
                    self.led_controller.clear()
                    self.logger.log("returned Result list = {}".format(action_result))
                elif action_result == "NoDisplay":
                    self.led_controller.show_non_result_display()
                elif action_result == "Unidentified":
                    self.led_controller.show_non_action_tag()
                elif action_result == "Progress":
                    goal_time = action_result_list["goal_total"]
                    total_time = action_result_list["time_spent"]
                    self.led_controller.start_progress(goal_time, total_time)

            self.logger.log("Exiting process_actions")

    def show_blue(self):
        self.led_controller.show_non_result_display()

    def log_tag(self, tag_id, start, end):
        self.tag_repository.log_tag(tag_id, self.device_id, start, end)


if __name__ == "__main__":
    from ledcontroller import LedController

    if len(sys.argv) == 2 and sys.argv[1] == "test":
        from mockrfireader import MockRfiReader
        # from mockapi import MockApi
        from timeularapi import TimularApi
        from debuglogger import DebugLogger
        from mockleddevice import MockLedDevice
        from tagrepository import TagRepository
        leddevice = MockLedDevice()
        logger = DebugLogger()
        reader = MockRfiReader()
        # api = MockApi()
        configuration = Configuration("debug_config.json")
        tag_repository = TagRepository(configuration)
        api = TimularApi(configuration, tag_repository, logger)
    else:
        from rfireader import RfiReader
        from timeularapi import TimularApi
        from logger import Logger
        from leddevice import LedDevice
        #from mockleddevice import MockLedDevice
        from tagrepository import TagRepository
        leddevice = LedDevice()
        logger = Logger()
        reader = RfiReader()
        configuration = Configuration("configuration.json")
        tag_repository = TagRepository(configuration)
        api = TimularApi(configuration, tag_repository, logger)

    actions = Actions(logger, TimeularAction(api, tag_repository, logger))
    dropTime = DropTime(LedController(leddevice), configuration, tag_repository, reader, actions, logger)
    dropTime.run()



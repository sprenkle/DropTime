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
        self.mlogger = my_logger
        self.none_count = 0
        self.tag_repository = tag_repository
        self.tag_start = None
        self.configuration = configuration
        self.device_id = self.configuration.get_value("device", "device_id")
        self.led_controller = led_controller

    def run(self):
        self.mlogger.log("started run")
        while True:
            self.process_actions()
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
        logger.log("card_id read is {}".format(card_id))
        if card_id is None:
            self.none_count = self.none_count + 1
        if card_id is not None:
            self.none_count = 0
        result_list = []
        if self.last_read != card_id and (card_id is not None or self.none_count > 2):
            logger.log("Tag changed tag_id={}".format(card_id))
            # we had a last read so we must log the stop time of the tag
            if self.last_read is not None:
                self.log_tag(self.last_read, self.tag_start, datetime.datetime.utcnow())

            # The tag_id is not null so we must give a start time
            if card_id is not None:
                self.tag_start = datetime.datetime.utcnow()

            self.mlogger.log("run - new id " + str(card_id))
            self.last_read = card_id

            result_list = self.actions.execute(card_id)

            if self.have_reminders():
                self.process_reminders()
            else:
                have_results = self.process_results(result_list)
                if not have_results:
                    if card_id is not None:
                        self.led_controller.show_non_result_display()
                        #print("show_non_result_display")
                else:
                    self.led_controller.show_non_action_tag()
            if card_id is None:
                self.led_controller.clear()
            logger.log("returned Result list = {}".format(have_results))
        logger.log("Exiting process_actions")
        return result_list

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



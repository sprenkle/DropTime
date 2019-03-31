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
            result_list = self.process_actions()
            if self.have_reminders():
                self.process_reminders()
            else:
                self.process_results(result_list)
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
                else:
                    self.led_controller.stop_progress()
                return  # this will only process first result with progress, re-look later

    def process_actions(self):
        card_id = self.reader.read_card()
        if card_id is None:
            self.none_count = self.none_count + 1
        if card_id is not None:
            self.none_count = 0
        if self.last_read != card_id and (card_id is not None or self.none_count > 2):
            # we had a last read so we must log the stop time of the tag
            if self.last_read is not None:
                self.log_tag(self.last_read, self.tag_start, datetime.datetime.utcnow())

            # The tag_id is not null so we must give a start time
            if card_id is not None:
                self.tag_start = datetime.datetime.utcnow()

            self.mlogger.log("run - new id " + str(card_id))
            self.last_read = card_id
            result_list = self.actions.execute(card_id)
            self.none_count = 0
            return result_list
        return []

    def log_tag(self, tag_id, start, end):
        self.tag_repository.log_tag(tag_id, self.device_id, start, end)


if __name__ == "__main__":
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
        from debuglogger import DebugLogger
        #from leddevice import LedDevice
        from mockleddevice import MockLedDevice
        from tagrepository import TagRepository

        leddevice = MockLedDevice()
        logger = DebugLogger()
        reader = RfiReader()
        configuration = Configuration("configuration.json")
        tag_repository = TagRepository(configuration)

        api = TimularApi(configuration, tag_repository, logger)

    actions = Actions(tag_repository, MockLedController(leddevice), logger, TimeularAction(api, tag_repository, logger))
    dropTime = DropTime(configuration, tag_repository, reader, actions, logger)
    dropTime.run()



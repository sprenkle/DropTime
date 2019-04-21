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
                self.reminder.have_tag(card_id)
                self.led_controller.show()
            except Exception as e:
                print(e)
                time.sleep(10)
            time.sleep(.1)

    def process_actions(self, card_id):

        if self.last_read != card_id:
            logging.info("Tag changed tag_id={}".format(card_id))
            # we had a last read so we must log the stop time of the tag
            if self.last_read is not None:
                self.log_tag(self.last_read, self.tag_start, datetime.datetime.utcnow())

            # The tag_id is not null so we must give a start time
            if card_id is not None:
                self.tag_start = datetime.datetime.utcnow()

            logging.info("run - new id " + str(card_id))
            self.last_read = card_id
            self.actions.execute(card_id)
            logging.debug("Exiting process_actions")

    def log_tag(self, tag_id, start, end):
        self.tag_repository.log_tag(tag_id, self.device_id, start, end)


if __name__ == "__main__":
    from ledcontroller import LedController

    if len(sys.argv) == 2 and sys.argv[1] == "test":
        from timeularapi import TimularApi
        from tagrepository import TagRepository
        from mockleddevice import MockLedDevice
        from mockrfireader import MockRfiReader
        led_device = MockLedDevice()
        led_controller = LedController(led_device)
        reader = MockRfiReader()
        configuration = Configuration("debug_config.json")
        tag_repository = TagRepository(configuration)
        api = TimularApi(configuration, tag_repository)
    else:
        from rfidevice import RfiDevice
        from timeularapi import TimularApi
        from leddevice import LedDevice
        from tagrepository import TagRepository
        configuration = Configuration("configuration.json")
        led_device = LedDevice(configuration)
        led_controller = LedController(led_device)
        reader = RfiDevice()
        tag_repository = TagRepository(configuration)
        api = TimularApi(configuration, tag_repository, led_controller)

    device_id = configuration.get_value("device", "device_id")
    actions = Actions(TimeularAction(api, tag_repository))
    dropTime = DropTime(led_controller, configuration, tag_repository, reader, actions, Reminder(tag_repository, device_id))
    dropTime.run()



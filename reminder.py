from datetime import datetime, timedelta
import logging


class Reminder:

    def __init__(self, tag_repository, device_id, led_controller):
        self.tags_seen = dict()
        self.active = []
        self.resolved = []
        self.tag_repository = tag_repository
        self.device_id = device_id
        self.next_start = None
        self.led_controller = led_controller
        self.has_reminder = False
        self.reminders = []
        self.next_update = datetime.now()
        self.device_id = device_id

    # updates the reminders from repository
    def update(self):
        if datetime.now() >= self.next_update:
            logging.info("Called reminder update deviceid={}".format(self.device_id))
            self.reminders = self.tag_repository.get_reminders(self.device_id)["reminders"]
            self.next_update = datetime.now() + timedelta(minutes=5)
            logging.info(self.reminders)

        logging.info("update called")
        current_dt = datetime.now()
        led_list = []
        for reminder in self.reminders:
            logging.info("Processing Reminder {}".format(reminder["name"]))
            dt = datetime.strptime(reminder["start"], "%Y-%m-%dT%H:%M:%S.000")
            dt = datetime(current_dt.year, current_dt.month, current_dt.day, dt.hour, dt.minute, dt.second)
            # if dt > current_dt:
            #     dt = dt - timedelta(days=1)
            duration = reminder["duration"]
            end_time = (dt + timedelta(seconds=duration))

            logging.info(self.tags_seen)

            if dt <= current_dt <= end_time:
                if reminder["reminderid"] in self.tags_seen and dt <= self.tags_seen[reminder["reminderid"]] <= end_time:
                    logging.info("Reminder Closed")
                else:
                    led_list.append(reminder["name"])
                    logging.info("Reminder Opened " + reminder["name"])
            else:
                logging.info("in reminder not inbetween time")

        if len(led_list) > 0:
            self.led_controller.set_reminder(led_list)
        else:
            self.led_controller.clear_reminder()

    def execute(self, tag_id):
        logging.info("Reminder tag_id = {}".format(tag_id))
        self.tag_repository.contains_id("2", tag_id, self.device_id)
        tag_to_action = self.tag_repository.tags_to_actions("2", tag_id)

        if tag_to_action is None:
            logging.info("No tag to action found")
            return

        self.tags_seen[tag_to_action["identifier"]] = datetime.now();

        logging.info("tags_to_action {} {}".format(tag_to_action["identifier"], self.tags_seen[tag_to_action["identifier"]]))

    def has_reminders(self):
        return len(self.reminders) > 0

    def process_reminders(self, card_id):
        logging.debug("process_reminders with tag_id = {}".format(card_id))
        if card_id is not None:
            self.tags_seen[str(card_id)] = datetime.now()


if __name__ == "__main__":
    from tagrepository import TagRepository
    from configuration import Configuration

    _configuration = Configuration("configuration.json")
    _device_id = _configuration.get_value("device", "device_id")
    _reminder = Reminder(TagRepository(_configuration), _device_id)
    _reminder.update()

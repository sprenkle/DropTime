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

    # updates the reminders from repository
    def update(self):
        if datetime.now() >= self.next_update:
            logging.info("Called reminder update")
            self.reminders = self.tag_repository.get_reminders(self.device_id)
            self.next_update = datetime.now() + timedelta(minutes=5)
            logging.info(self.device_id)
            logging.info(self.reminders)
            logging.info(self.next_update)
            logging.debug(self.reminders)

        logging.info("update called")
        current_dt = datetime.now()
        led_list = []
        for reminder in self.reminders:
            dt = datetime.strptime(reminder["start"], "%Y-%m-%dT%H:%M:%S.000")
            dt = datetime(current_dt.year, current_dt.month, current_dt.day, dt.hour, dt.minute, dt.second)
            if dt > current_dt:
                dt = dt - timedelta(days=1)
            duration = reminder["duration"]
            end_time = (dt + timedelta(seconds=duration))
            if reminder["tagid"] in self.tags_seen:
                tag_time = self.tags_seen[reminder["tagid"]]
            else:
                tag_time = None
            logging.info(self.tags_seen)
            logging.info("{} <= {} <= {}  --  {} <= {} <= {}".format(dt, current_dt, end_time, dt, tag_time, end_time))
            if dt <= current_dt <= end_time and (reminder["tagid"] not in self.tags_seen or
                                                 not (dt <= self.tags_seen[reminder["tagid"]] <= end_time )):
                display = list(eval(reminder["display"]))
                for led_value in display:
                    led_list.append(led_value)

        if len(led_list) > 0:
            while len(led_list) < 24:
                led_list += led_list
            self.led_controller.set_reminder(led_list[0:24])
        else:
            self.led_controller.clear_reminder()

    def execute(self, tag_id):
        self.tags_seen[tag_id] = datetime.now();

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

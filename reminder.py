from datetime import datetime, timedelta


class Reminder:

    def __init__(self, tag_repository, device_id):
        self.reminders = []
        self.active = []
        self.resolved = []
        self.tag_repository = tag_repository
        self.last_update = None
        self.device_id = device_id
        self.next_start = None

    # updates the reminders from repository
    def update(self):
        self.reminders = self.tag_repository.get_reminders(self.device_id)

    # returns array of led values
    def get_display(self):
        current_dt = datetime.now()
        led_list = []
        for reminder in self.reminders:
            dt = datetime.strptime(reminder["start"], "%Y-%m-%dT%H:%M:%S.000")
            dt = datetime(current_dt.year, current_dt.month, current_dt.day, dt.hour, dt.second)

            print(dt.time())
            print((timedelta(seconds=reminder["duration"]) + dt).time())

            if dt > current_dt:
                dt = dt - timedelta(day=1)

            if dt <= current_dt <= timedelta(seconds=reminder["duration"]) + dt:
                led_list.append(reminder[""])
                print("In time")


            # hour = reminder["start"].hour
            # minute = reminder["start"].minute
            # second = reminder["start"].seconds
            # print("{} {} {}".format(hour, minute, second))

    # will be called when a tag is active
    def have_tag(self, tag_id):
        pass


if __name__ == "__main__":
    from tagrepository import TagRepository
    from configuration import Configuration

    _configuration = Configuration("configuration.json")
    _device_id = _configuration.get_value("device", "device_id")
    _reminder = Reminder(TagRepository(_configuration), _device_id)
    _reminder.update()
    _reminder.get_display()

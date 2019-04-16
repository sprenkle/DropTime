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

    def has_reminders(self):
        return len(self.reminders) > 0

    # returns array of led values
    def get_display(self):
        current_dt = datetime.now()
        led_list = []
        for reminder in self.reminders:
            dt = datetime.strptime(reminder["start"], "%Y-%m-%dT%H:%M:%S.000")
            dt = datetime(current_dt.year, current_dt.month, current_dt.day, dt.hour, dt.second)
            if dt > current_dt:
                dt = dt - timedelta(day=1)

            if dt <= current_dt <= timedelta(seconds=reminder["duration"]) + dt:
                if reminder in self.resolved:
                    continue
                led_list.append(reminder["display"])
            else:
                if reminder in self.resolved:
                    self.resolved.remove(reminder)

        return led_list


    # will be called when a tag is active
    def have_tag(self, tag_id):
        for reminder in self.reminders:
            if reminder["tagid"] == tag_id and reminder not in self.resolved:
                self.resolved.append(reminder)


if __name__ == "__main__":
    from tagrepository import TagRepository
    from configuration import Configuration

    _configuration = Configuration("configuration.json")
    _device_id = _configuration.get_value("device", "device_id")
    _reminder = Reminder(TagRepository(_configuration), _device_id)
    _reminder.update()
    print(_reminder.get_display())

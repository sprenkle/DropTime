from datetime import datetime, timedelta


class Reminder:

    def __init__(self, tag_repository, device_id, led_controller):
        self.reminders = []
        self.active = []
        self.resolved = []
        self.tag_repository = tag_repository
        self.last_update = None
        self.device_id = device_id
        self.next_start = None
        self.led_controller = led_controller

    # updates the reminders from repository
    def update(self):
        self.reminders = self.tag_repository.get_reminders(self.device_id)
        self.get_display()

    def has_reminders(self):
        return len(self.reminders) > 0

    def have_tag(self, tag_id):
        for reminder in self.reminders:
            if reminder["tagid"] == tag_id and reminder not in self.resolved:
                self.resolved.append(reminder)

    def get_display(self):
        current_dt = datetime.now()
        led_list = []
        for reminder in self.reminders:
            dt = datetime.strptime(reminder["start"], "%Y-%m-%dT%H:%M:%S.000")
            dt = datetime(current_dt.year, current_dt.month, current_dt.day, dt.hour, dt.minute, dt.second)
            if dt > current_dt:
                dt = dt - timedelta(days=1)
            duration = reminder["duration"]
            end_time = (dt + timedelta(seconds=duration))
            if dt <= current_dt <= end_time:
                if reminder in self.resolved:
                    continue
                led_list.append(reminder["display"])
            else:
                if reminder in self.resolved:
                    self.resolved.remove(reminder)
        if len(led_list) > 0:
            self.led_controller.set_reminder(led_list)
        else:
            self.led_controller.clear_reminder()

    def process_reminders(self, card_id):
        self.have_tag(card_id)
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


if __name__ == "__main__":
    from tagrepository import TagRepository
    from configuration import Configuration
    from ledcontroller import LedController
    from mockleddevice import MockLedDevice

    _configuration = Configuration("configuration.json")
    _device_id = _configuration.get_value("device", "device_id")
    _reminder = Reminder(TagRepository(_configuration), _device_id, LedController(MockLedDevice))
    _reminder.update()
    print(_reminder.get_display())

class Reminder:

    def __init__(self, tag_repository, device_id):
        self.reminder_list = dict()
        self.active = dict()
        self.resolved = dict()
        self.tag_repository = tag_repository
        self.last_update = None
        self.device_id = device_id

    # updates the reminders from repository
    def update(self):
        reminders = self.tag_repository.get_reminders(self.device_id)
        for reminder in reminders:
            pass

    # returns array of led values
    def get_display(self):
        pass

    # will be called when a tag is active
    def have_tag(self, tag_id):
        pass




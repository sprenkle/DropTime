class TimeularAction:

    def __init__(self, api):
        self.task_dict = {231965344320: "369007", 438308258332: "369008", 25991398012: "369006"}
        self.running_tag_id = None
        self.api = api

    def is_actionable(self, tag_id):
        return tag_id in self.task_dict or tag_id is None

    def execute(self, tag_id):
        if tag_id is None:
            if self.running_tag_id is not None:
                self.api.stop_tracking(self.task_dict[self.running_tag_id])
                self.running_tag_id = None
            return
        if tag_id not in self.task_dict:
            print(tag_id + " Not Valid")
            return
        self.running_tag_id = tag_id
        self.api.start_tracking(self.task_dict[tag_id])

class TimeularAction:

    def __init__(self, api, card_repository):
        self.running_tag_id = None
        self.api = api
        self.card_repository = card_repository

    def is_actionable(self, tag_id):
        return self.card_repository.contains_id(tag_id)

    def execute(self, tag_id):
        if tag_id is None:
            if self.running_tag_id is not None:
                self.api.stop_tracking(self.card_repository.activity_id(self.running_tag_id))
                self.running_tag_id = None
            return
        if tag_id not in self.task_dict:
            print(tag_id + " Not Valid")
            return
        self.running_tag_id = tag_id
        self.api.start_tracking(self.task_dict[tag_id])

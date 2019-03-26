class TimeularAction:

    def __init__(self, api, tag_repository):
        self.running_tag_id = None
        self.api = api
        self.tag_repository = tag_repository
        self.user_to_token_dict = dict()

    def execute(self, tag_id):
        if tag_id is None or not self.tag_repository.contains_id(tag_id):
            if self.running_tag_id is not None:
                self.api.stop_tracking(self.tag_repository.activity_id(self.running_tag_id))
                self.running_tag_id = None
            return
        self.running_tag_id = tag_id
        activity = self.tag_repository.activity(tag_id);
        if tag_id not in self.user_to_token_dict:
            # get token and add
            token = self.tag_repository.get_token(activity["userid"])
            self.user_to_token_dict[activity["userid"]] = token

        self.api.start_tracking(token, activity)

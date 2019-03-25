class TimeularAction:

    def __init__(self, api, card_repository):
        self.running_tag_id = None
        self.api = api
        self.card_repository = card_repository
        self.user_to_token_dict = dict()

    def execute(self, tag_id):
        if tag_id is None or not self.card_repository.contains_id(tag_id):
            if self.running_tag_id is not None:
                self.api.stop_tracking(self.card_repository.activity_id(self.running_tag_id))
                self.running_tag_id = None
            return
        self.running_tag_id = tag_id
        activity = self.card_repository.activity(tag_id);
        if tag_id not in self.user_to_token_dict:
            # get token and add
            token = card_repository.get_token(activity["userid"])

        self.api.start_tracking(token, activity)

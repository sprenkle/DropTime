class TimeularAction:

    def __init__(self, api, tag_repository):
        self.running_tag_id = None
        self.api = api
        self.tag_repository = tag_repository
        self.user_to_token_dict = dict()

    def execute(self, tag_id):
        # If running tag is not None and does not equal tag_id then stop last activity
        if self.running_tag_id is not None and self.running_tag_id != tag_id:
            self.api.stop_tracking(self.tag_repository.activity_id(self.running_tag_id))

        # If tag_id is None then set running tag and return
        if tag_id is None:
            self.running_tag_id = None
            return

        # check if tag has a activity
        if not self.tag_repository.contains_id(tag_id):
            self.running_tag_id = None
            return

        # have activity start it
        self.running_tag_id = tag_id
        # todo working on this
        activity = self.tag_repository.activity(tag_id);
        if tag_id not in self.user_to_token_dict:
            # get token and add
            user_id = activity["userid"]
            api_key, api_secret = self.tag_repository.get_api_key_token(user_id)
            token = self.api.get_token(api_key, api_secret)
            self.user_to_token_dict[user_id] = token
        else:
            token = self.user_to_token_dict[activity["userid"]]

        self.api.start_tracking(token, activity)

class PillAction:

    def __init__(self, api, tag_repository):
        self.running_tag_id = None
        self.api = api
        self.tag_repository = tag_repository
        self.user_to_token_dict = dict()
        self.id = 1

    def get_id(self):
        return self.id

    def poll(self, tag_id):
        pass

    def execute(self, tag_id):
        # If running tag is not None and does not equal tag_id then stop last activity
        if self.running_tag_id is not None and self.running_tag_id != tag_id:
            if self.tag_repository.contains_id(self.running_tag_id):
                activity = self.tag_repository.tags_to_actions(self.running_tag_id)
                token = self.get_token(activity["userid"])
                self.api.stop_tracking(token, activity["identifier"])

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
        activity = self.tag_repository.tags_to_actions(tag_id)
        user_id = activity["userid"]
        token = self.get_token(user_id)
        self.api.start_tracking(token, activity["identifier"])


    def get_token(self, user_id):
        if user_id not in self.user_to_token_dict:
            # get token and add
            api_key, api_secret = self.tag_repository.get_api_key_token(user_id)
            token = self.api.get_token(api_key, api_secret)
            self.user_to_token_dict[user_id] = token
            return token
        else:
            return self.user_to_token_dict[user_id]

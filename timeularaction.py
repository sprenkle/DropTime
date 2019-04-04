class TimeularAction:

    def __init__(self, api, tag_repository, logger):
        self.running_tag_id = None
        self.api = api
        self.tag_repository = tag_repository
        self.user_to_token_dict = dict()
        self.id = 1
        self.logger = logger

    def get_id(self):
        return self.id

    def poll(self, tag_id):
        return {}

    def execute(self, tag_id):
        self.logger.log("tag_id = {}  running_tag_id={}".format(tag_id, self.running_tag_id))
        # If running tag is not None and does not equal tag_id then stop last activity
        if self.running_tag_id is not None and self.running_tag_id != tag_id:
            if self.tag_repository.contains_id(self.id, self.running_tag_id):
                activity = self.tag_repository.activity(self.id, self.running_tag_id)
                token = self.get_token(activity["userid"])
                self.api.stop_tracking(token, activity["identifier"])

        # If tag_id is None then set running tag and return
        if tag_id is None:
            self.logger.log("tag_id is none, returning")
            self.running_tag_id = None
            return {"ActionReturnType": "Unidentified"}

        # check if tag has a activity
        if not self.tag_repository.contains_id(self.id, tag_id):
            self.logger.log("tag is not in repository, returning")
            self.running_tag_id = None
            return {"ActionReturnType": "Unidentified"}

        # have activity start it
        self.running_tag_id = tag_id
        # todo working on this
        activity = self.tag_repository.activity(self.id, tag_id)
        user_id = activity["userid"]
        token = self.get_token(user_id)
        self.logger.log("start tracking")
        self.api.start_tracking(token, activity["identifier"])
        if activity["dailygoals"] == 1:
            return {"ActionReturnType": "Progress", "goal_total": activity["dailytimeSec"], "current_time": 0}
        return {"ActionReturnType": "NoDisplay"}

    def get_token(self, user_id):
        if user_id not in self.user_to_token_dict:
            # get token and add
            api_key, api_secret = self.tag_repository.get_api_key_token(user_id)
            token = self.api.get_token(api_key, api_secret)
            self.user_to_token_dict[user_id] = token
            return token
        else:
            return self.user_to_token_dict[user_id]

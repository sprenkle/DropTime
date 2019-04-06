import datetime

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
                tag_to_action = self.tag_repository.tags_to_actions(self.id, self.running_tag_id)
                token = self.get_token(tag_to_action["userid"])
                self.api.stop_tracking(token, tag_to_action["identifier"])

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
        tag_to_action = self.tag_repository.tags_to_actions(self.id, tag_id)
        user_id = tag_to_action["userid"]
        token = self.get_token(user_id)
        self.logger.log("start tracking")
        self.api.start_tracking(token, tag_to_action["identifier"])
        activity = self.tag_repository.get_activity(tag_to_action["identifier"])
        print(activity)

        if ("show" in activity and activity["show"] == 0) or "dailygoals" not in activity:
            return {"ActionReturnType": "NoDisplay"}

        time_spent = 0
        if activity["dailygoals"] == 1: # reset each time you use it, like a timer
            return {"ActionReturnType": "Progress", "goal_total": activity["dailytimeSec"], "time_spent": time_spent}

        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day

        if activity["show"] == 2: # for each day
            start_time = datetime.datetime(year, month, day, 0, 0, 0)
            duration = self.tag_repository.get_activity_duration(1, tag_to_action["identifier"], start_time,
                                                                 datetime.datetime.utcnow())
            return {"ActionReturnType": "Progress", "goal_total": activity["dailytimeSec"], "time_spent": duration}



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

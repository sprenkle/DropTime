import datetime
import logging


class TimeularAction:

    def __init__(self, api, tag_repository, led_controller):
        self.running_tag_id = None
        self.api = api
        self.tag_repository = tag_repository
        self.user_to_token_dict = dict()
        self.id = 1
        self.led_controller = led_controller

    def get_id(self):
        return self.id

    def poll(self, tag_id):
        return {}

    def execute(self, tag_id):
        logging.debug("tag_id = {}  running_tag_id={}".format(tag_id, self.running_tag_id))

        self.stop_running_tag(tag_id)

        if tag_id is None:
            return self.current_tag_is_none()

        if not self.tag_repository.contains_id(self.id, tag_id):
            return self.current_tag_not_in_repository()

        # have activity start it
        self.running_tag_id = tag_id
        # todo working on this
        tag_to_action = self.tag_repository.tags_to_actions(self.id, tag_id)
        user_id = tag_to_action["userid"]
        token = self.get_token(user_id)
        logging.info("start tracking")
        self.api.start_tracking(token, tag_to_action["identifier"])
        activity = self.tag_repository.get_activity(tag_to_action["identifier"])
        print(activity)

        if ("show" in activity and activity["show"] == 0) or "dailygoals" not in activity or \
                "" == activity["dailygoals"]:
            self.led_controller.set_have_tracking_tag()

        time_spent = 0

        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour

        if activity["dailygoals"] == 1:  # reset each time you use it, like a timer
            pass
        elif activity["dailygoals"] == 2:  # for each hour
            start_time = datetime.datetime(year, month, day, hour, 0, 0)
            time_spent = self.tag_repository.get_activity_duration(1, tag_to_action["identifier"], start_time,
                                                                   datetime.datetime.utcnow())
        elif activity["dailygoals"] == 3:  # for each day
            start_time = datetime.datetime(year, month, day, 0, 0, 0)
            time_spent = self.tag_repository.get_activity_duration(1, tag_to_action["identifier"], start_time,
                                                                   datetime.datetime.utcnow())
        elif activity["dailygoals"] == 4:  # for each week
            week = now.weekday()

            start_time = datetime.datetime(year, month, day - week, 0, 0, 0)
            time_spent = self.tag_repository.get_activity_duration(1, tag_to_action["identifier"], start_time,
                                                                   datetime.datetime.utcnow())
        elif activity["dailygoals"] == 5:  # for each month
            start_time = datetime.datetime(year, month, 0, 0, 0, 0)
            time_spent = self.tag_repository.get_activity_duration(1, tag_to_action["identifier"], start_time,
                                                                   datetime.datetime.utcnow())
        elif activity["dailygoals"] == 6:  # for each year
            start_time = datetime.datetime(year, 0, 0, 0, 0, 0)
            time_spent = self.tag_repository.get_activity_duration(1, tag_to_action["identifier"], start_time,
                                                                   datetime.datetime.utcnow())
        elif activity["dailygoals"] == 7:  # total lifetime
            start_time = datetime.datetime.min
            time_spent = self.tag_repository.get_activity_duration(1, tag_to_action["identifier"], start_time,
                                                                   datetime.datetime.utcnow())

        self.led_controller.set_progress(self, activity["dailytimeSec"], time_spent)

    def get_token(self, user_id):
        if user_id not in self.user_to_token_dict:
            # get token and add
            api_key, api_secret = self.tag_repository.get_api_key_token(user_id)
            token = self.api.get_token(api_key, api_secret)
            self.user_to_token_dict[user_id] = token
            return token
        else:
            return self.user_to_token_dict[user_id]

    def stop_running_tag(self, tag_id):
        if self.running_tag_id is not None and self.running_tag_id != tag_id:
            if self.tag_repository.contains_id(self.id, self.running_tag_id):
                tag_to_action = self.tag_repository.tags_to_actions(self.id, self.running_tag_id)
                token = self.get_token(tag_to_action["userid"])
                self.api.stop_tracking(token, tag_to_action["identifier"])

    def current_tag_is_none(self):
        logging.info("tag_id is none, returning")
        self.running_tag_id = None
        self.led_controller.clear_tag()

    def current_tag_not_in_repository(self):
        logging.info("tag is not in repository, returning")
        self.running_tag_id = None
        self.led_controller.set_unknown_tag()

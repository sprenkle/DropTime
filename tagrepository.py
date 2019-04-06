import requests
import sys
from datetime import datetime
from configuration import Configuration


class TagRepository:

    def __init__(self, configuration):
        self.base_url = configuration.get_value("tag_api", "url")
        print(self.base_url)
        self.tags_to_action_dict = {}

    def contains_id(self, action_type, tag_id):
        url = self.base_url + '/tagstoactions/' + str(action_type) + '/' + str(tag_id)
        print("url is {}".format(url))
        r = requests.get(url)
        activity = r.json()
        if activity is None:
            return False
        print(activity)
        self.add_tags_to_action(action_type, tag_id, activity)
        return True

    def tags_to_actions(self, action_type, tag_id):
        if action_type not in self.tags_to_action_dict:
            return None
        action_dict = self.tags_to_action_dict[action_type]
        if tag_id not in action_dict:
            return None
        return action_dict[tag_id]

    def add_tags_to_action(self, action_type, tag_id, activity):
        if action_type not in self.tags_to_action_dict:
            self.tags_to_action_dict = self.tags_to_action_dict[action_type] = dict()
        action_dict = self.tags_to_action_dict[action_type]
        action_dict[tag_id] = activity

    def get_api_key_token(self, user_id):
        url = self.base_url + '/users/' + str(user_id)
        r = requests.get(url)
        user = r.json()
        return user["username"], user["userpassword"]

    def get_activity(self, activity_id):
        url = self.base_url + '/activities/' + str(activity_id)
        r = requests.get(url)
        activity = r.json()
        return activity

    def get_activity_duration(self, activity_type, activity_id, start, end):
        start_str = datetime.strftime(start, '%Y-%m-%dT%H:%M:%S.000')
        end_str = datetime.strftime(end, '%Y-%m-%dT%H:%M:%S.000')
        url = self.base_url + "/taglog/{}/{}/start/{}/end/{}".format(activity_type, activity_id, start_str, end_str)
        print("url is {}".format(url))
        r = requests.get(url)
        activity = r.json()
        if activity is None:
            return 0
        duration = activity["duration"]
        return duration

    def log_tag(self, tag_id, device_id, start, end):
        start_str = datetime.strftime(start, '%Y-%m-%dT%H:%M:%S.000')
        end_str = datetime.strftime(end, '%Y-%m-%dT%H:%M:%S.000')
        duration = (end - start).total_seconds()
        url = self.base_url + '/taglog'
        # body = "{tagid1:'{}', 'deviceid':'{}', 'start': '{}', " \
        #        "'stop': '{}', 'totaltimes': {}}".format(tag_id, device_id, start_str, end_str, duration)
        body = {'tagid': tag_id, 'deviceid': device_id, 'start': start_str, 'stop': end_str, 'totaltimes': duration}
        r = requests.post(url, json=body)
        return r.json()


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        file = "debug_config.json"
    else:
        file = "configuration.json"
    # {231965344320: "369007", 438308258332: "369008", 25991398012: "369006"}
    card_repository = TagRepository(Configuration(file))
    print(card_repository.get_api_key_token(1))

   # print(card_repository.activity_id(231965344320))

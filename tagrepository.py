import requests
import sys
from configuration import Configuration


class TagRepository:

    def __init__(self, configuration):
        self.base_url = configuration.get_value("tag_api", "url")
        print(self.base_url)
        self.activity_dict = {}

    def contains_id(self, action_type, tag_id):
        url = self.base_url + '/tagstoactions/' + str(action_type) + '/' + str(tag_id)
        print("url is {}".format(url))
        r = requests.get(url)
        activity = r.json()
        if activity is None:
            return False
        print(activity)
        self.add_activity(action_type, tag_id, activity)
        return True

    def activity(self, action_type, tag_id):
        if action_type not in self.activity_dict:
            return None
        action_dict = self.activity_dict[action_type]
        if tag_id not in action_dict:
            return None
        return action_dict[tag_id]

    def add_activity(self, action_type, tag_id, activity):
        if action_type not in self.activity_dict:
            self.activity_dict = self.activity_dict[action_type] = dict()
        action_dict = self.activity_dict[action_type]
        action_dict[tag_id] = activity

    def get_api_key_token(self, user_id):
        url = self.base_url + '/users/' + str(user_id)
        r = requests.get(url)
        user = r.json()
        return user["username"], user["userpassword"]

    def get_tag_duration(self, tag_id, start, end):
        def logtag(self, tag_id, start, end, duration):
            url = self.base_url + '/tagstoactions/' + str(action_type) + '/' + str(tag_id)
            print("url is {}".format(url))
            r = requests.get(url)
            activity = r.json()
        return 100

    def log_tag(self, tagid, start, end, duration):
        pass

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        file = "debug_config.json"
    else:
        file = "configuration.json"
    # {231965344320: "369007", 438308258332: "369008", 25991398012: "369006"}
    card_repository = TagRepository(Configuration(file))
    print(card_repository.get_api_key_token(1))

   # print(card_repository.activity_id(231965344320))

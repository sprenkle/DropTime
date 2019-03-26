import requests
import sys
from configuration import Configuration


class TagRepository:

    def __init__(self, configuration):
        self.base_url = configuration.get_value("tag_api", "url")
        print(self.base_url)
        self.activity_dict = {}

    def contains_id(self, tag_id):
        url = self.base_url + '/tagstoactions/' + str(tag_id)
        print("url is {}".format(url))
        r = requests.get(url)
        activity = r.json()
        if activity is None:
            return False
        print(activity)
        self.activity_dict[tag_id] = activity
        return True

    def activity(self, tag_id):
        return self.activity_dict[tag_id]

    def get_api_key_token(self, user_id):
        url = self.base_url + '/users/' + str(user_id)
        r = requests.get(url)
        user = r.json()
        return user["username"], user["userpassword"]


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        file = "debug_config.json"
    else:
        file = "configuration.json"
    # {231965344320: "369007", 438308258332: "369008", 25991398012: "369006"}
    card_repository = TagRepository(Configuration(file))
    print(card_repository.get_api_key_token(1))

   # print(card_repository.activity_id(231965344320))

import requests


class CardRepository:

    def __init__(self):
        self.base_url = "http://David-Tower:5002"
        self.activity_dict = {}

    def contains_id(self, tag_id):
        url = self.base_url + '/tagstoactions/' + str(tag_id)
        r = requests.get(url)
        activity = r.json()
        self.activity_dict[tag_id] = activity
        return activity

    def activity(self, tag_id):
        return self.activity_dict[tag_id]

    def get_token(self, user_id):
        url = self.base_url + '/users/' + str(user_id)
        r = requests.get(url)
        activity = r.json()
        return activity



if __name__ == "__main__":
    # {231965344320: "369007", 438308258332: "369008", 25991398012: "369006"}
    card_repository = CardRepository()
    print(card_repository.contains_id(231965344320))

    print(card_repository.activity_id(231965344320))
